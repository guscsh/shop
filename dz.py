#Static Folder Name
folder_name = "" 

dz_array = {
        "public":{
            "favicon":f"{folder_name}/images/favicon.png",
            "keywords":"Nova",
            "description":"Nova",
            "og_title":"Nova",
            "og_description":"Nova",
            "og_image":"",
            "title":"Nova",
        },
        "global": {
            "css": [
                f"{folder_name}/vendor/bootstrap-select/dist/css/bootstrap-select.min.css",
                f"{folder_name}/vendor/swiper/swiper-bundle.min.css",
                f"{folder_name}/vendor/nouislider/nouislider.min.css",
                f"{folder_name}/vendor/animate/animate.css",
                f"{folder_name}/vendor/lightgallery/dist/css/lightgallery.css",
                f"{folder_name}/vendor/lightgallery/dist/css/lg-thumbnail.css",
                f"{folder_name}/vendor/lightgallery/dist/css/lg-zoom.css",
                f"{folder_name}/css/style.css",
            ],
            "js": {
                "top": [
                    f"{folder_name}/js/jquery.min.js",
                    f"{folder_name}/vendor/wow/wow.min.js",
                    f"{folder_name}/vendor/bootstrap/dist/js/bootstrap.bundle.min.js",
                    f"{folder_name}/vendor/bootstrap-select/dist/js/bootstrap-select.min.js",
                ],
                "bottom": [
                    f"{folder_name}/vendor/bootstrap-touchspin/bootstrap-touchspin.js",
                    f"{folder_name}/vendor/counter/waypoints-min.js",
                    f"{folder_name}/vendor/counter/counterup.min.js",
                    f"{folder_name}/vendor/swiper/swiper-bundle.min.js",
                    f"{folder_name}/vendor/imagesloaded/imagesloaded.js",
                    f"{folder_name}/vendor/masonry/masonry-4.2.2.js",
                    f"{folder_name}/vendor/masonry/isotope.pkgd.min.js",
                    f"{folder_name}/vendor/countdown/jquery.countdown.js",
                    f"{folder_name}/vendor/wnumb/wNumb.js",
                    f"{folder_name}/vendor/nouislider/nouislider.min.js",
                    f"{folder_name}/js/dz.carousel.js",
                    f"{folder_name}/js/dz.ajax.js",
                    f"{folder_name}/js/custom.js",
                ],
            },
        },
        "pagelevel":{
            # AppName
            "pages":{
                "views":{
                    # file type
                    "css":{
                        # name from urls.py
                        "index": [
                        ],
                        "about": [
                        ],
                        "blog": [
                        ],
                        "blog_post": [
                        ],
                        "shop_list": [
                        ],
                    },
                    "js":{
                        "index": [
                            f"{folder_name}/vendor/magnific-popup/magnific-popup.js",
                            f"{folder_name}/vendor/lightgallery/dist/lightgallery.min.js",
                            f"{folder_name}/vendor/lightgallery/dist/plugins/thumbnail/lg-thumbnail.min.js",
                            f"{folder_name}/vendor/lightgallery/dist/plugins/zoom/lg-zoom.min.js",
                        ],
                        "about": [
                        ],
                        "blog": [
                        ],
                        "blog_post": [
                        ],
                        "shop_list": [
                            f"{folder_name}/vendor/lightgallery/dist/lightgallery.min.js",
                            f"{folder_name}/vendor/lightgallery/dist/plugins/thumbnail/lg-thumbnail.min.js",
                            f"{folder_name}/vendor/lightgallery/dist/plugins/zoom/lg-zoom.min.js",
                        ],
                        "test": [
                            f"{folder_name}/vendor/magnific-popup/magnific-popup.js",
                            f"{folder_name}/vendor/lightgallery/dist/lightgallery.min.js",
                            f"{folder_name}/vendor/lightgallery/dist/plugins/thumbnail/lg-thumbnail.min.js",
                            f"{folder_name}/vendor/lightgallery/dist/plugins/zoom/lg-zoom.min.js",
                        ]
                    },
                },
            },
            # AppName
            "products":{
                "views":{
                    # file type
                    "css":{
                        # name from urls.py
                        "list": [
                        ],
                        "pages": [
                        ],
                    },
                    "js":{
                        "list": [
                        ],
                        "pages": [
                        ],
                    },
                },
            },
            # AppName
            "accounts":{
                "views":{
                    # file type
                    "css":{
                        # name from urls.py
                        "register": [
                        ],
                        "login": [
                        ],
                        "logout": [
                        ],
                        "profile": [
                        ],
                    },
                    "js":{
                        "register": [
                        ],
                        "login": [
                        ],
                        "logout": [
                        ],
                        "profile": [
                        ],
                    },
                },
            },
            # "pixio":{
            #     "views":{
            #         "js":{
            #             "index": [
            #                 f"{folder_name}/vendor/magnific-popup/magnific-popup.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/lightgallery.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/thumbnail/lg-thumbnail.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/zoom/lg-zoom.min.js",
            #             ],
            #             "index_2": [
            #                 f"{folder_name}/vendor/magnific-popup/magnific-popup.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/lightgallery.min.js",
            #                 f"{folder_name}/vendor/group-slide/group-loop.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/thumbnail/lg-thumbnail.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/zoom/lg-zoom.min.js",
            #             ],
            #             "index_3": [
            #                 f"{folder_name}/vendor/magnific-popup/magnific-popup.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/lightgallery.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/thumbnail/lg-thumbnail.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/zoom/lg-zoom.min.js",
            #                 f"{folder_name}/vendor/skrollr/skrollr.js",
            #             ],
            #             "shop_standard": [
            #                 f"{folder_name}/vendor/lightgallery/dist/lightgallery.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/thumbnail/lg-thumbnail.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/zoom/lg-zoom.min.js",
            #             ],
            #             "shop_list": [
            #                 f"{folder_name}/vendor/lightgallery/dist/lightgallery.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/thumbnail/lg-thumbnail.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/zoom/lg-zoom.min.js",
            #             ],
            #             "shop_with_category": [
            #                 f"{folder_name}/vendor/lightgallery/dist/lightgallery.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/thumbnail/lg-thumbnail.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/zoom/lg-zoom.min.js",
            #             ],
            #             "shop_filters_top_bar": [
            #                 f"{folder_name}/vendor/lightgallery/dist/lightgallery.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/thumbnail/lg-thumbnail.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/zoom/lg-zoom.min.js",
            #             ],
            #             "shop_sidebar": [
            #                 f"{folder_name}/vendor/lightgallery/dist/lightgallery.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/thumbnail/lg-thumbnail.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/zoom/lg-zoom.min.js",
            #             ],
            #             "shop_style_1": [
            #                 f"{folder_name}/vendor/lightgallery/dist/lightgallery.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/thumbnail/lg-thumbnail.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/zoom/lg-zoom.min.js",
            #             ],
            #             "shop_style_2": [
            #                 f"{folder_name}/vendor/lightgallery/dist/lightgallery.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/thumbnail/lg-thumbnail.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/zoom/lg-zoom.min.js",
            #             ],
            #             "product_default": [
            #                 f"{folder_name}/js/jquery.star-rating-svg.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/lightgallery.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/thumbnail/lg-thumbnail.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/zoom/lg-zoom.min.js",
            #             ],
            #             "product_thumbnail": [
            #                 f"{folder_name}/js/jquery.star-rating-svg.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/lightgallery.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/thumbnail/lg-thumbnail.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/zoom/lg-zoom.min.js",
            #             ],
            #             "product_grid_media": [
            #                 f"{folder_name}/js/jquery.star-rating-svg.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/lightgallery.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/thumbnail/lg-thumbnail.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/zoom/lg-zoom.min.js",
            #             ],
            #             "product_carousel": [
            #                 f"{folder_name}/js/jquery.star-rating-svg.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/lightgallery.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/thumbnail/lg-thumbnail.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/zoom/lg-zoom.min.js",
            #             ],
            #             "product_full_width": [
            #                 f"{folder_name}/js/jquery.star-rating-svg.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/lightgallery.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/thumbnail/lg-thumbnail.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/zoom/lg-zoom.min.js",
            #             ],
            #             "shop_wishlist": [
            #             ],
            #             "shop_cart": [
            #             ],
            #             "shop_checkout": [
            #             ],
            #             "shop_compare": [
            #             ],
            #             "shop_order_tracking": [
            #             ],
            #             "shop_my_account": [
            #             ],
            #             "shop_registration": [
            #                 f"{folder_name}/vendor/lightgallery/dist/lightgallery.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/thumbnail/lg-thumbnail.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/zoom/lg-zoom.min.js",
            #             ],
            #             "blog_dark_2_column": [
            #             ],
            #             "blog_dark_2_column_sidebar": [
            #             ],
            #             "blog_dark_3_column_sidebar": [
            #             ],
            #             "blog_dark_half_image": [
            #             ],
            #             "blog_light_2_column": [
            #             ],
            #             "blog_light_2_column_sidebar": [
            #             ],
            #             "blog_light_half_image": [
            #             ],
            #             "blog_exclusive": [
            #             ],
            #             "blog_left_sidebar": [
            #             ],
            #             "blog_right_sidebar": [
            #             ],
            #             "blog_both_sidebar": [
            #             ],
            #             "blog_wide_sidebar": [
            #             ],
            #             "blog_archive": [
            #             ],
            #             "blog_author": [
            #             ],
            #             "blog_category": [
            #             ],
            #             "blog_tag": [
            #             ],
            #             "post_standard": [
            #             ],
            #             "post_left_sidebar": [
            #             ],
            #             "post_header_image": [
            #                 f"{folder_name}/vendor/magnific-popup/magnific-popup.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/lightgallery.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/thumbnail/lg-thumbnail.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/zoom/lg-zoom.min.js",
            #             ],
            #             "post_slide_show": [
            #             ],
            #             "post_side_image": [
            #             ],
            #             "post_gallery": [
            #             ],
            #             "post_gallery_alternative": [
            #             ],
            #             "post_open_gutenberg": [
            #                 f"{folder_name}/vendor/magnific-popup/magnific-popup.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/lightgallery.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/thumbnail/lg-thumbnail.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/zoom/lg-zoom.min.js",
            #             ],
            #             "post_link": [
            #             ],
            #             "post_audio": [
            #             ],
            #             "post_video": [
            #             ],
            #             "portfolio_tiles": [
            #             ],
            #             "collage_style_1": [
            #             ],
            #             "collage_style_2": [
            #             ],
            #             "masonry_grid": [
            #             ],
            #             "cobble_style_1": [
            #             ],
            #             "cobble_style_2": [
            #             ],
            #             "portfolio_thumbs_slider": [
            #             ],
            #             "portfolio_film_strip": [
            #             ],
            #             "carousel_showcase": [
            #             ],
            #             "portfolio_split_slider": [
            #                 f"{folder_name}/vendor/multiscroll/easing.js",
            #                 f"{folder_name}/vendor/multiscroll/jquery.multiscroll.min.js",
            #             ],
            #             "portfolio_details_1": [
            #                 f"{folder_name}/vendor/magnific-popup/magnific-popup.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/lightgallery.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/thumbnail/lg-thumbnail.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/zoom/lg-zoom.min.js",
            #             ],
            #             "portfolio_details_2": [
            #                 f"{folder_name}/vendor/magnific-popup/magnific-popup.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/lightgallery.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/thumbnail/lg-thumbnail.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/zoom/lg-zoom.min.js",
            #             ],
            #             "portfolio_details_3": [
            #                 f"{folder_name}/vendor/magnific-popup/magnific-popup.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/lightgallery.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/thumbnail/lg-thumbnail.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/zoom/lg-zoom.min.js",
            #             ],
            #             "portfolio_details_4": [
            #                 f"{folder_name}/vendor/magnific-popup/magnific-popup.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/lightgallery.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/thumbnail/lg-thumbnail.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/zoom/lg-zoom.min.js",
            #             ],
            #             "portfolio_details_5": [
            #                 f"{folder_name}/vendor/magnific-popup/magnific-popup.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/lightgallery.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/thumbnail/lg-thumbnail.min.js",
            #                 f"{folder_name}/vendor/lightgallery/dist/plugins/zoom/lg-zoom.min.js",
            #             ],
            #             "about_us": [
            #             ],
            #             "about_me": [
            #             ],
            #             "pricing_table": [
            #             ],
            #             "our_gift_vouchers": [
            #             ],
            #             "what_we_do": [
            #             ],
            #             "faq_1": [
            #             ],
            #             "faq_2": [
            #             ],
            #             "our_team": [
            #             ],
            #             "contact_us_1": [
            #             ],
            #             "contact_us_2": [
            #             ],
            #             "contact_us_3": [
            #             ],
            #             "error_404": [
            #             ],
            #             "error_2": [
            #             ],
            #             "coming_soon": [
            #             ],
            #             "under_construct": [
            #             ],
            #             "banner_with_bg_color": [
            #             ],
            #             "banner_with_image": [
            #             ],
            #             "banner_with_video": [
            #             ],
            #             "banner_with_kanbern": [
            #             ],
            #             "banner_small": [
            #             ],
            #             "banner_medium": [
            #             ],
            #             "banner_large": [
            #             ],
            #             "header_style_1": [
            #             ],
            #             "header_style_2": [
            #             ],
            #             "header_style_3": [
            #             ],
            #             "header_style_4": [
            #             ],
            #             "header_style_5": [
            #             ],
            #             "header_style_6": [
            #             ],
            #             "header_style_7": [
            #             ],
            #             "footer_style_1": [
            #             ],
            #             "footer_style_2": [
            #             ],
            #             "footer_style_3": [
            #             ],
            #             "footer_style_4": [
            #             ],
            #             "footer_style_5": [
            #             ],
            #             "footer_style_6": [
            #             ],
            #             "footer_style_7": [
            #             ],
            #             "account_dashboard": [
            #                 f"{folder_name}/vendor/apexchart/apexchart.js",
            #                 f"{folder_name}/js/dashbord-account.js",
            #             ],
            #             "account_orders": [
            #             ],
            #             "account_order_details": [
            #             ],
            #             "account_order_confirmation": [
            #             ],
            #             "account_downloads": [
            #             ],
            #             "account_return_request": [
            #             ],
            #             "account_return_request_details": [
            #             ],
            #             "account_refund_request_confirmed": [
            #             ],
            #             "account_profile": [
            #             ],
            #             "account_address": [
            #             ],
            #             "account_shipping_methods": [
            #             ],
            #             "account_payment_methods": [
            #             ],
            #             "account_review": [
            #             ],
            #             "account_billing_address": [
            #             ],
            #             "account_shipping_address": [
            #             ],
            #             "account_cancellation_requests": [
            #             ],
            #         },
            #     }
            # }
        }
}