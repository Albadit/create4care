#if ANDROID
using JsPermissionHandler;
#endif

namespace create4care
{
    public partial class MainPage : ContentPage
    {
        public MainPage()
        {
            InitializeComponent();

            #if ANDROID
            new BlazorWebViewHandler()            
                .AddCamera()
                .AddInitializingHandler(blazorWebView);
            #endif
        }
    }
}
