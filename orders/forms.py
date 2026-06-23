from django import forms


class CheckoutForm(forms.Form):  # 用 Form 是需要先驗證再由 service 處理。如果用 ModelForm 則是先存入資料庫再由 service 處理。
    # 驗證通過後，這些值會被「快照」複製到 Order 模型對應欄位，
    # 避免日後使用者改 profile 影響歷史訂單的收件資料。
    full_name = forms.CharField(max_length=150, label='Full Name')  
    email = forms.EmailField(label='Email')                          
    phone = forms.CharField(max_length=20, label='Phone')            
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label='Address')  

    # 只有卡號末四碼會透過 get_payment_data() 取出後傳給 services。
    card_number = forms.CharField(max_length=19, label='Card Number')   
    card_expiry = forms.CharField(max_length=7, label='Expiry MM/YY')   
    card_cvc = forms.CharField(max_length=4, label='CVC')              

    def clean_card_number(self):
        # 取出原始輸入並移除所有空白
        card = self.cleaned_data['card_number'].replace(' ', '')

        # 檢查：必須全為數字、長度至少 13 碼（信用卡最小長度規範）
        if not card.isdigit() or len(card) < 13:
            raise forms.ValidationError('Invalid card number.')

        # 回傳清洗後的版本，會覆寫 cleaned_data['card_number']
        return card

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        # 只有在「有登入使用者」且「表單尚未綁定資料」時才預填
        if user and not self.is_bound:
            # 用 getattr 安全取得 profile（OneToOne 關聯不存在時不會炸）
            profile = getattr(user, 'profile', None)

            # full_name：優先用「姓 + 名」，若兩者皆空則 fallback 到 username
            self.fields['full_name'].initial = (
                f'{user.first_name} {user.last_name}'.strip() or user.username
            )

            # email 直接取 user.email
            self.fields['email'].initial = user.email

            # 若使用者有 profile，再預填電話與地址
            if profile:
                self.fields['phone'].initial = profile.phone
                self.fields['address'].initial = profile.address

        # 統一為所有欄位加上 Bootstrap form-control class
        # 用 setdefault 而非直接賦值：保留欄位本身已自帶的 class，不覆蓋
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')

    def get_payment_data(self):
        # 取出已清洗過（去空格）的卡號
        card = self.cleaned_data['card_number']

        # 只回傳末四碼與付款方式，完整卡號不會離開此方法
        return {
            'method': 'credit_card',
            'card_last_four': card[-4:],
        }