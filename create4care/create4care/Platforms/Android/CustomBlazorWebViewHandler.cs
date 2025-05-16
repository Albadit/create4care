using Android.Webkit;
using Microsoft.AspNetCore.Components.WebView.Maui;

namespace create4care
{
    public class CustomBlazorWebViewHandler : BlazorWebViewHandler
    {
        protected override Android.Webkit.WebView CreatePlatformView()
        {
            var webView = base.CreatePlatformView();
            webView.Settings.MediaPlaybackRequiresUserGesture = false;
            webView.SetWebChromeClient(new GrantAllPermissionsChromeClient());
            return webView;
        }
    }

    class GrantAllPermissionsChromeClient : WebChromeClient
    {
        public override void OnPermissionRequest(PermissionRequest? request)
        {
            if (request is null) return;
            request.Grant(request.GetResources());
        }
    }
}
