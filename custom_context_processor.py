from dz import dz_array

def dz_static(request):

    context = {                         # 建立一個安全的預設基礎字典
        "dz_array": dz_array,
        "current_page_css": [],
        "current_page_js": [],
        "preloader":"preloader-1",      # select style for preloader
        "header":"header-1",            # select style for header
        "footer":"footer-1"             # select style for footer
    }
        
    match = request.resolver_match      # 獲取當前請求的路由解析資訊
    
    if match:
        app_name = match.app_name       # 會抓到 "pages"、"products" 或 "accounts"
        view_name = match.url_name      # 會抓到 "index"、"shop_list" 等 View 內的 Function 名字
        
        try:                            # 從 dz_array 撈出對應 App 的對應 View 資源，然後將撈到的 CSS 和 JS 放入 context
            pagelevel_data = dz_array["pagelevel"][app_name]["views"]
            context["current_page_css"] = pagelevel_data["css"].get(view_name, [])
            context["current_page_js"] = pagelevel_data["js"].get(view_name, [])

        except KeyError:                # 如果目前身處的 App 或是 View 沒寫在 dz.py 清單裡，就默默跳過（放空清單）
            pass
            
    return context