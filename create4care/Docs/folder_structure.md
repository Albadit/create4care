# Folder structure
```
C:\Users\ardit\Documents\GitHub\School\year_3\sem6\create4care\create4care
├── App.xaml
├── App.xaml.cs
├── Components
│   ├── Layout
│   │   ├── MainLayout.razor
│   │   └── MainLayout.razor.css
│   ├── Models
│   │   ├── NavMenuModels.cs
│   │   └── Slides.cs
│   ├── Pages
│   │   ├── Bluetooth.razor
│   │   ├── Home.razor
│   │   ├── Instruction.razor
│   │   ├── Measuring.razor
│   │   ├── Settings.razor
│   │   └── Test.razor
│   ├── Routes.razor
│   ├── Services
│   │   └── BluetoothService.cs
│   ├── Shared
│   │   └── NavMenu.razor
│   └── _Imports.razor
├── MainPage.xaml
├── MainPage.xaml.cs
├── MauiProgram.cs
├── Properties
│   └── launchSettings.json
├── create4care.csproj
├── create4care.csproj.user
├── create4care.sln
└── wwwroot
    ├── css
    │   └── app.css
    ├── index.html
    └── js
        ├── mediapipePose.js
        └── test.js
```

## App.xaml
```xaml
﻿<?xml version="1.0" encoding="UTF-8" ?>
<Application xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
             xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
             xmlns:local="clr-namespace:create4care"
             x:Class="create4care.App">
    <Application.Resources>
        <ResourceDictionary>

        <!--
            For information about styling .NET MAUI pages
            please refer to the documentation:
            https://go.microsoft.com/fwlink/?linkid=2282329
        -->

        </ResourceDictionary>
    </Application.Resources>
</Application>

```

## App.xaml.cs
```cs
﻿namespace create4care
{
    public partial class App : Application
    {
        public App()
        {
            InitializeComponent();
        }

        protected override Window CreateWindow(IActivationState? activationState)
        {
            return new Window(new MainPage()) { Title = "create4care" };
        }
    }
}

```

## Components/Layout/MainLayout.razor
```razor
﻿@inherits LayoutComponentBase

@Body

```

## Components/Layout/MainLayout.razor.css
```css

```

## Components/Models/NavMenuModels.cs
```cs
using Microsoft.AspNetCore.Components;

namespace create4care.Components.Models;

public class NavItem
{
    public string Name { get; set; }
    public string Href { get; set; }
    public RenderFragment Icon { get; set; }
}

public class MenuSection
{
    public string Header { get; set; }
    public List<NavItem> NavItems { get; set; }
}

public class NavMenuModel
{
    public List<MenuSection> MenuSections { get; set; }
}
```

## Components/Models/Slides.cs
```cs
using Microsoft.AspNetCore.Components;

namespace create4care.Components.Models;

public class SlidePage
{
    public RenderFragment Image { get; set; }
    public string Title { get; set; }
    public string Content { get; set; }
}

```

## Components/Pages/Bluetooth.razor
```razor
﻿@page "/bluetooth"
@inject BluetoothService BluetoothService

<NavMenu Name="Bluetooth"/>

<main>
    <label>Connect to Arduino BLE:</label>
    <button class="btn" @onclick="ConnectToDevice" disabled="@(isConnecting || isConnected)">
        @(isConnected ? "Connected" : (isConnecting ? "Connecting..." : "Connect"))
    </button>

    <p>@statusMessage</p>
    <p>@dataMessage</p>
</main>

@code {
    private bool isConnecting = false;
    private bool isConnected = false;
    private string statusMessage = "Status: Not connected";
    private string dataMessage = "No data yet";

    protected override void OnInitialized()
    {
        BluetoothService.OnStatusChanged += UpdateStatus;
        BluetoothService.OnDataReceived += UpdateData;
    }

    private async Task ConnectToDevice()
    {
        if (isConnected) return;

        isConnecting = true;
        statusMessage = "Scanning for devices...";
        StateHasChanged();

        await BluetoothService.ConnectAsync();

        isConnecting = false;
        StateHasChanged();
    }

    private void UpdateStatus(string status)
    {
        statusMessage = status;

        if (status.Contains("Connected"))
        {
            isConnected = true;
        }
        else if (status.Contains("not found") || status.Contains("Error"))
        {
            isConnected = false;
        }

        InvokeAsync(StateHasChanged);
    }

    private void UpdateData(string data)
    {
        dataMessage = data;
        InvokeAsync(StateHasChanged);
    }
}

<style>
main {
    display: flex;
    flex-direction: column;
    gap: 20px;
}
</style>

```

## Components/Pages/Home.razor
```razor
﻿@page "/"

<NavMenu Name="Home"/>

<main>
    <h1>Hello, world!</h1>

    <span>Welcome to your new app.</span>

    <div class="loader"></div>
</main>

<style>
main {
    display: flex;
    flex-direction: column;
    gap: 20px;
}
</style>
```

## Components/Pages/Instruction.razor
```razor
﻿@page "/instruction"
@inject NavigationManager Navigation

<NavMenu Name="Instruction"/>

<main style="
    --ani-fade: @AniFade; 
    --ani-slide-offset: @AniSlideOffset; 
    --indicator-width: @($"{DotWidth}px"); 
    --indicator-active-width:@($"{IndicatorActiveWidth}px"); 
    --indicator-gap: @($"{IndicatorGap}px");
    ">
    <div class="slider-container">
        <div class="slider-background">
            <IconBackgroundShape />
            <div class="slider-page @AnimationClass">@Pages[CurrentPageIndex].Image</div>
        </div>
        <div class="slider-content">
            <h2 class="slider-page @AnimationClass">@Pages[CurrentPageIndex].Title</h2>
            <p class="slider-page @AnimationClass">@Pages[CurrentPageIndex].Content</p>
        </div>
    </div>

    <div class="actions">
        @* <div class="indicators">
            @for (int i = 0; i < Pages.Count; i++)
            {
                <span class="indicator @(i == CurrentPageIndex ? "active" : "")"></span>
            }
        </div> *@

        <div class="indicators">
            <span class="active-indicator" style="@($"left: {ComputeIndicatorLeft()}px;")"></span>
            @for (int i = 0; i < Pages.Count; i++)
            {
                <span class="indicator @(i == CurrentPageIndexAnimation ? $"active {(isReversedTransition ? "back" : "next")}" : "")"></span>
            }
        </div>

        <div class="buttons">
            <button @onclick="PreviousPage" disabled="@(CurrentPageIndexAnimation == 0)" class="btn btn-secondary btn-back @(CurrentPageIndexAnimation != 0 ? "btn-back-active" : "")">
                Back
            </button>
            <button @onclick="NextPage" class="btn">Next</button>
        </div>
    </div>
</main>

@code {
    private List<SlidePage> Pages = new List<SlidePage>
    {
        new SlidePage
        {
            Image = @<IconPerson />,
            Title = "Step 1: This is the title of the onboarding", 
            Content = "Lorem ipsum dolor sit amet, consectetur adipiscing elit ut aliquam, purus sit amet luctus venenatis"
        },
        new SlidePage
        {
            Image = @<IconCamera />,
            Title = "Step 2: This is the title of the onboarding",
            Content = "Lorem ipsum dolor sit amet, consectetur adipiscing elit ut aliquam, purus sit amet luctus venenatis"
        },
        new SlidePage
        {
            Image = @<IconPerson />,
            Title = "Step 3: This is the title of the onboarding",
            Content = "Lorem ipsum dolor sit amet, consectetur adipiscing elit ut aliquam, purus sit amet luctus venenatis"
        },
        new SlidePage
        {
            Image = @<IconPerson />,
            Title = "Step 4: This is the title of the onboarding",
            Content = "Lorem ipsum dolor sit amet, consectetur adipiscing elit ut aliquam, purus sit amet luctus venenatis"
        }
    };

    private int CurrentPageIndex = 0;
    private int CurrentPageIndexAnimation = 0;
    private bool IsAnimating = false;
    private string AnimationClass = "";
    private int FadeDuration = 500;
    private int WaitDuration = 0;
    private bool isReversedTransition = false;

    private string AniFade => $"{FadeDuration / 1000.0}s";
    private string AniSlideOffset => "20px";
    private const double IndicatorGap = 15;
    private const double IndicatorActiveWidth = 28;
    private const double DotWidth = 6;

    private async Task AnimateTransition(Func<int, int> updatePage)
    {
        CurrentPageIndexAnimation = updatePage(CurrentPageIndex);
        AnimationClass = isReversedTransition ? "fade-out-reverse" : "fade-out";
        StateHasChanged();
        await Task.Delay(FadeDuration + WaitDuration);

        CurrentPageIndex = updatePage(CurrentPageIndex);

        AnimationClass = isReversedTransition ? "fade-in-reverse" : "fade-in";
        StateHasChanged();
        await Task.Delay(FadeDuration);

        AnimationClass = "";
        IsAnimating = false;
    }

    private async Task NextPage()
    {
        if (IsAnimating) return;
        if (CurrentPageIndex == Pages.Count - 1)
        {
            Navigation.NavigateTo("/");
            return;
        }
        IsAnimating = true;
        isReversedTransition = false;
        await AnimateTransition(i => i + 1);
    }

    private async Task PreviousPage()
    {
        if (IsAnimating) return;
        IsAnimating = true;
        isReversedTransition = true;
        await AnimateTransition(i => i > 0 ? i - 1 : i);
    }

    private double ComputeIndicatorLeft() => CurrentPageIndexAnimation * (DotWidth + IndicatorGap);
}

<style>
main {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.slider-container {
    width: 100%;
    position: relative;
    display: flex;
    gap: 40px;
    flex-direction: column;
    align-items: center;
    flex-grow: 1;
}

.slider-background {
    position: relative;
    height: max-content;
    width: max-content;
}

.slider-background > svg {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-58%, -46%);
    fill: var(--clr-primary);
    width: fit-content;
    z-index: -1;
}

.slider-content {
    display: flex;
    flex-direction: column;
    gap: 20px;
    text-align: center;
}

.slider-content > h1 {
    color: var(--clr-text);
    font-size: 26px;
}

.slider-content > p {
    color: var(--clr-text-tint);
    font-size: 15px;
}

/* Base state for slider pages */
.slider-page {
    opacity: 1;
    transform: translateX(0);
}


@@keyframes fadeOutSlide {
    from { opacity: 1; transform: translateX(0); }
    to { opacity: 0; transform: translateX(calc(0px - var(--ani-slide-offset))); }
}
.slider-page.fade-out {
    animation: fadeOutSlide var(--ani-fade) ease forwards;
}

@@keyframes fadeInSlide {
    from { opacity: 0; transform: translateX(var(--ani-slide-offset)); }
    to { opacity: 1; transform: translateX(0); }
}
.slider-page.fade-in {
    animation: fadeInSlide var(--ani-fade) ease forwards;
}

@@keyframes fadeOutSlideReverse {
    from { opacity: 1; transform: translateX(0); }
    to { opacity: 0; transform: translateX(var(--ani-slide-offset)); }
}
.slider-page.fade-out-reverse {
    animation: fadeOutSlideReverse var(--ani-fade) ease forwards;
}

@@keyframes fadeInSlideReverse {
    from { opacity: 0; transform: translateX(calc(0px - var(--ani-slide-offset))); }
    to { opacity: 1; transform: translateX(0); }
}
.slider-page.fade-in-reverse {
    animation: fadeInSlideReverse var(--ani-fade) ease forwards;
}

.actions {
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 25px;
}

.indicators {
    display: flex;
    flex-direction: row;
    gap: var(--indicator-gap);
    justify-content: center;
    align-items: center;
    position: relative;
}

.indicator {
    width: var(--indicator-width);
    height: var(--indicator-width);
    border-radius: 10px;
    background-color: var(--clr-indicator);
}

@* .indicator.active {
    width: var(--indicator-active-width);
} *@

.indicator.active.back {
    margin-right: calc(var(--indicator-active-width) / 2 + var(--indicator-width));
}

.indicator.active.next {
    margin-left: calc(var(--indicator-active-width) / 2 + var(--indicator-width));
}

.active-indicator {
    position: absolute;
    top: 0;
    left: 0;
    height: var(--indicator-width);
    width: var(--indicator-active-width);
    background-color: var(--clr-primary);
    border-radius: 10px;
    transition: left var(--ani-fade) ease, transform var(--ani-fade) ease;
}

.buttons {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    gap: 20px;
    width: 100%;
    max-width: 500px;
}

.btn-back {
    opacity: 0;
    transition: opacity var(--ani-fade) ease;
}

.btn-back-active {
    opacity: 1;
}
</style>

```

## Components/Pages/Measuring.razor
```razor
﻿@page "/measuring"
@inject IJSRuntime JS

<NavMenu Name="Measuring" />

<main>
    <h1>Measuring with Pose Detection</h1>

    <span id="loading" style="display: block; text-align: center;">Loading camera...</span>
    <span id="error" style="display: none; color: red; text-align: center;"></span>

    <div id="counter"></div>
    <div id="notification"></div>

    <div id="container">
        <video id="videoInput" playsinline></video>
        <canvas id="output"></canvas>
    </div>
</main>

@code {
    protected override async Task OnAfterRenderAsync(bool firstRender)
    {
        if (firstRender)
        {
            await JS.InvokeVoidAsync("startMediapipePose");
        }
    }
}

<style>
main {
    display: flex;
    flex-direction: column;
    gap: 20px;
    overflow: auto;
}

#counter {
    font-size: 30px;
    color: white;
    text-align: center;
    margin-bottom: 10px;
    visibility: hidden;
}

#notification {
    font-size: 30px;
    color: green;
    text-align: center;
    margin-bottom: 10px;
    display: none;
}

#container {
    position: relative;
    width: 100%;
    height: 100%;
    overflow: hidden; /* Crop overflowing canvas */
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 10px;
}

video {
    display: none;
}

canvas {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}
</style>
```

## Components/Pages/Settings.razor
```razor
﻿@page "/settings"
@using Microsoft.Maui.Storage

<NavMenu Name="Settings"/>

<main>
    <label>Enter api url:</label>
        <input class="inp"
            type="text"
            placeholder="https://dummyjson.com/users/1"
            @bind="apiUrl"
            disabled="@isSaving" />

    <button class="btn"
            disabled="@isSaving"
            @onclick="SaveApiUrl">
        @(isSaving ? "Saving..." : "Save")
    </button>

    @if (!string.IsNullOrEmpty(feedbackMessage))
    {
        <p>@feedbackMessage</p>
    }
</main>

@code {
    private string apiUrl { get; set; }
    private bool isSaving = false;
    private string feedbackMessage;

    protected override void OnInitialized()
    {
        apiUrl = Preferences.Get("ApiUrl", "");
    }

    private async Task SaveApiUrl()
    {
        isSaving = true;
        feedbackMessage = string.Empty;
        StateHasChanged();

        await Task.Delay(500);

        Preferences.Set("ApiUrl", apiUrl);

        isSaving = false;
        feedbackMessage = "API URL saved successfully!";
        StateHasChanged();
    }
}

<style>
main {
    display: flex;
    flex-direction: column;
    gap: 20px;
}
</style>
```

## Components/Pages/Test.razor
```razor
﻿@page "/test"
@inject IJSRuntime JS

<NavMenu Name="Test" />

<main>
    <h1>Measuring with Pose Detection</h1>

    <div id="container">
        <video id="input_video"></video>
        <canvas id="output_canvas"></canvas>
    </div>
</main>

@code {
    protected override async Task OnAfterRenderAsync(bool firstRender)
    {
        if (firstRender)
        {
            await JS.InvokeVoidAsync("mediapipePose");
        }
    }
}
```

## Components/Routes.razor
```razor
﻿<Router AppAssembly="@typeof(MauiProgram).Assembly">
    <Found Context="routeData">
        <RouteView RouteData="@routeData" DefaultLayout="@typeof(Layout.MainLayout)" />
    </Found>
</Router>

```

## Components/Services/BluetoothService.cs
```cs
﻿using Plugin.BLE;
using Plugin.BLE.Abstractions.Contracts;
using Plugin.BLE.Abstractions.EventArgs;
using System;
using System.Text;
using System.Threading.Tasks;

namespace create4care.Components.Services;

public class BluetoothService
{
    IAdapter _adapter;
    IBluetoothLE _ble;
    IDevice _device;
    IService _service;
    ICharacteristic _characteristic;

    // Convert 16-bit UUIDs to full 128-bit format.
    Guid serviceUuid = Guid.Parse("0000180C-0000-1000-8000-00805F9B34FB");
    Guid characteristicUuid = Guid.Parse("00002A56-0000-1000-8000-00805F9B34FB");

    // Events to notify the UI
    public event Action<string> OnStatusChanged;
    public event Action<string> OnDataReceived;

    public BluetoothService()
    {
        _ble = CrossBluetoothLE.Current;
        _adapter = CrossBluetoothLE.Current.Adapter;
    }

    public async Task ConnectAsync()
    {
        OnStatusChanged?.Invoke("Scanning for devices...");
        try
        {
            _adapter.DeviceDiscovered += (s, a) =>
            {
                if (!string.IsNullOrEmpty(a.Device.Name) &&
                    a.Device.Name.Equals("Arduino_R4_WiFi", StringComparison.Ordinal))
                {
                    _device = a.Device;
                }
            };

            await _adapter.StartScanningForDevicesAsync();

            if (_device == null)
            {
                OnStatusChanged?.Invoke("Device not found.");
                return;
            }

            OnStatusChanged?.Invoke($"Connecting to {_device.Name}...");
            await _adapter.ConnectToDeviceAsync(_device);

            int mtu = await _device.RequestMtuAsync(50);
            System.Diagnostics.Debug.WriteLine($"MTU requested: {mtu}");

            _service = await _device.GetServiceAsync(serviceUuid);
            if (_service == null)
            {
                OnStatusChanged?.Invoke("Service not found.");
                return;
            }

            _characteristic = await _service.GetCharacteristicAsync(characteristicUuid);
            if (_characteristic == null)
            {
                OnStatusChanged?.Invoke("Characteristic not found.");
                return;
            }

            if (_characteristic.CanUpdate)
            {
                _characteristic.ValueUpdated += Characteristic_ValueUpdated;
                await _characteristic.StartUpdatesAsync();
                OnStatusChanged?.Invoke("Connected. Waiting for data...");
            }
            else
            {
                OnStatusChanged?.Invoke("Characteristic doesn't support notifications.");
            }
        }
        catch (Exception ex)
        {
            OnStatusChanged?.Invoke($"Error: {ex.Message}");
        }
    }

    private void Characteristic_ValueUpdated(object sender, CharacteristicUpdatedEventArgs e)
    {
        // Convert the incoming byte array (JSON data) to a string.
        string json = Encoding.UTF8.GetString(e.Characteristic.Value);
        OnDataReceived?.Invoke(json);
    }
}

```

## Components/Shared/NavMenu.razor
```razor
﻿<header>
    <input type="checkbox" id="toggleSidebar">
    <div class="header-title">
        <label for="toggleSidebar" class="hamburger-menu">
            <span></span>
            <span></span>
            <span></span>
        </label>
        <span>@Name</span>
    </div>
    <div class="sidebar">
        <div class="content">
            <nav class="nav-header">
                @foreach (var menuSection in navMenuModel.MenuSections)
                {
                    <section>
                        <span>@menuSection.Header</span>
                        @foreach (var item in menuSection.NavItems)
                        {
                            <NavLink href="@item.Href" draggable="false" Match="@(item.Href == "/" ? NavLinkMatch.All : NavLinkMatch.Prefix)">
                                @item.Icon
                                @item.Name
                            </NavLink>
                        }
                    </section>
                }
            </nav>
            <nav class="nav-footer">
                @foreach (var item in navMenuFooterItems)
                {
                    <NavLink href="@item.Href" draggable="false">
                        @item.Icon
                        @item.Name
                    </NavLink>
                }
            </nav>
        </div>
        <label for="toggleSidebar" class="close-sidebar"></label>
    </div>
</header>

@code {
    [Parameter]
    public string Name { get; set; } = "Page";

    NavMenuModel navMenuModel = new NavMenuModel
    {
        MenuSections = new List<MenuSection>
        {
            new MenuSection
            {
                Header = "Overview",
                NavItems = new List<NavItem>
                {
                    new NavItem { Name = "Home", Href = "/", Icon = @<IconHome /> },
                    new NavItem { Name = "Bluetooth", Href = "/bluetooth", Icon = @<IconBluetooth /> },
                    new NavItem { Name = "Instruction", Href = "/instruction", Icon = @<IconInstruction /> },
                    new NavItem { Name = "Measuring", Href = "/measuring", Icon =  @<IconMeasuring /> },
                    new NavItem { Name = "Settings", Href = "/settings", Icon = @<IconSettings /> },
                    new NavItem { Name = "Test", Href = "/test", Icon = @<IconSettings /> }
                }
            }
        }
    };

    List<NavItem> navMenuFooterItems = new List<NavItem>
    {
        new NavItem { Name = "Help & Information", Href = "/help", Icon = @<IconInfo /> },
        new NavItem { Name = "Log Out", Href = "/logout", Icon = @<IconLogout /> },
        new NavItem { Name = "Login", Href = "/login", Icon = @<IconLogin /> },
    };
}

<style>
/* Toggle and Header */
#toggleSidebar { 
    display: none; 
}

.header-title {
    display: flex;
    align-items: center;
    gap: 20px;
}

.header-title > span { 
    font-weight: 600;
    font-size: 20px;
}

/* Hamburger Menu */
.hamburger-menu {
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 4px;
    padding: 10px;
    margin: -10px;
}

.hamburger-menu span {
    width: 22px;
    height: 2px;
    border-radius: 5px;
    background-color: var(--clr-hamburger-menu);
}

/* Sidebar and Content */
.sidebar {
    z-index: 100;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100dvh;
    display: flex;
    pointer-events: none;
    transition: background-color 0.3s ease;
}

.content {
    width: max-content;
    padding: 20px 26px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background: var(--clr-background);
    transform: translateX(-100%);
    transition: transform 0.3s ease;
    pointer-events: auto;
}

.close-sidebar {
    flex: 1;
    cursor: pointer;
}

#toggleSidebar:checked ~ .sidebar {
    pointer-events: auto;
    background-color: var(--clr-link);
}

#toggleSidebar:checked ~ .sidebar > .content {
    transform: translateX(0);
}

/* Navigation */
.nav-header {
    overflow: auto;
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.nav-header section {
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.sidebar span {
    font-weight: 500;
    padding: 10px 0;
    font-size: 14px;
    color: var(--clr-text-menu);
}

.sidebar a {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 12px;
    border-radius: 8px;
    color: var(--clr-text-menu);
    text-decoration: none;
}

.nav-header a { 
    font-weight: 600; 
}

.nav-footer a { 
    font-weight: 500;
}

.nav-footer svg,
.nav-footer svg path,
.nav-footer svg rect,
.nav-footer svg circle,
.nav-footer svg ellipse,
.nav-footer svg line,
.nav-footer svg polygon,
.nav-footer svg polyline
{
    stroke-width: 1.2px;
}

.sidebar svg {
    width: 22px;
    fill: var(--clr-text-menu);
}

/* Images and Hover/Active States */
.sidebar a:hover,
.active {
    background-color: var(--clr-link);
    color: var(--clr-text) !important;
}

.sidebar a:hover svg,
.active svg {
    fill: var(--clr-text) !important;
}
</style>
```

## Components/_Imports.razor
```razor
﻿@using System.Net.Http
@using System.Net.Http.Json
@using Microsoft.AspNetCore.Components.Forms
@using Microsoft.AspNetCore.Components.Routing
@using Microsoft.AspNetCore.Components.Web
@using Microsoft.AspNetCore.Components.Web.Virtualization
@using Microsoft.JSInterop
@using create4care
@using create4care.Components
@using create4care.Components.Shared
@using create4care.Components.Shared.Icon
@using create4care.Components.Services
@using create4care.Components.Models

```

## MainPage.xaml
```xaml
﻿<?xml version="1.0" encoding="utf-8" ?>
<ContentPage xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
             xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
             xmlns:local="clr-namespace:create4care"
             x:Class="create4care.MainPage">

    <BlazorWebView x:Name="blazorWebView" HostPage="wwwroot/index.html">
        <BlazorWebView.RootComponents>
            <RootComponent Selector="#app" ComponentType="{x:Type local:Components.Routes}" />
        </BlazorWebView.RootComponents>
    </BlazorWebView>

</ContentPage>

```

## MainPage.xaml.cs
```cs
﻿using Microsoft.Maui.ApplicationModel; // already added at the top of your file
using Microsoft.Maui.Controls;

namespace create4care
{
    public partial class MainPage : ContentPage
    {
        public MainPage()
        {
            InitializeComponent();
        }
    }
}

```

## MauiProgram.cs
```cs
﻿using Microsoft.Extensions.Logging;
using create4care.Components.Services;
using Microsoft.Maui.Handlers;

namespace create4care;

public static class MauiProgram
{
	public static MauiApp CreateMauiApp()
	{
		var builder = MauiApp.CreateBuilder();
		builder
			.UseMauiApp<App>()
			.ConfigureFonts(fonts =>
			{
				fonts.AddFont("OpenSans-Regular.ttf", "OpenSansRegular");
			});


		builder.Services.AddMauiBlazorWebView();
        builder.Services.AddSingleton<BluetoothService>();
#if DEBUG
        builder.Services.AddBlazorWebViewDeveloperTools();
		builder.Logging.AddDebug();
#endif
		return builder.Build();
	}
}

```

## Properties/launchSettings.json
```json
{
  "profiles": {
    "Windows Machine": {
      "commandName": "Project",
      "nativeDebugging": false
    }
  }
}
```

## create4care.csproj
```csproj
﻿<Project Sdk="Microsoft.NET.Sdk.Razor">

    <PropertyGroup>
        <TargetFrameworks>net9.0-android;net9.0-ios;net9.0-maccatalyst</TargetFrameworks>
        <TargetFrameworks Condition="$([MSBuild]::IsOSPlatform('windows'))">$(TargetFrameworks);net9.0-windows10.0.19041.0</TargetFrameworks>
        <!-- Uncomment to also build the tizen app. You will need to install tizen by following this: https://github.com/Samsung/Tizen.NET -->
        <!-- <TargetFrameworks>$(TargetFrameworks);net9.0-tizen</TargetFrameworks> -->

        <!-- Note for MacCatalyst:
            The default runtime is maccatalyst-x64, except in Release config, in which case the default is maccatalyst-x64;maccatalyst-arm64.
            When specifying both architectures, use the plural <RuntimeIdentifiers> instead of the singular <RuntimeIdentifier>.
            The Mac App Store will NOT accept apps with ONLY maccatalyst-arm64 indicated;
            either BOTH runtimes must be indicated or ONLY macatalyst-x64. -->
        <!-- For example: <RuntimeIdentifiers>maccatalyst-x64;maccatalyst-arm64</RuntimeIdentifiers> -->

        <OutputType>Exe</OutputType>
        <RootNamespace>create4care</RootNamespace>
        <UseMaui>true</UseMaui>
        <SingleProject>true</SingleProject>
        <ImplicitUsings>enable</ImplicitUsings>
        <EnableDefaultCssItems>false</EnableDefaultCssItems>
        <Nullable>enable</Nullable>

        <!-- Display name -->
        <ApplicationTitle>create4care</ApplicationTitle>

        <!-- App Identifier -->
        <ApplicationId>com.companyname.create4care</ApplicationId>

        <!-- Versions -->
        <ApplicationDisplayVersion>1.0</ApplicationDisplayVersion>
        <ApplicationVersion>1</ApplicationVersion>

        <!-- To develop, package, and publish an app to the Microsoft Store, see: https://aka.ms/MauiTemplateUnpackaged -->
        <WindowsPackageType>None</WindowsPackageType>

        <SupportedOSPlatformVersion Condition="$([MSBuild]::GetTargetPlatformIdentifier('$(TargetFramework)')) == 'ios'">15.0</SupportedOSPlatformVersion>
        <SupportedOSPlatformVersion Condition="$([MSBuild]::GetTargetPlatformIdentifier('$(TargetFramework)')) == 'maccatalyst'">15.0</SupportedOSPlatformVersion>
        <SupportedOSPlatformVersion Condition="$([MSBuild]::GetTargetPlatformIdentifier('$(TargetFramework)')) == 'android'">24.0</SupportedOSPlatformVersion>
        <SupportedOSPlatformVersion Condition="$([MSBuild]::GetTargetPlatformIdentifier('$(TargetFramework)')) == 'windows'">10.0.17763.0</SupportedOSPlatformVersion>
        <TargetPlatformMinVersion Condition="$([MSBuild]::GetTargetPlatformIdentifier('$(TargetFramework)')) == 'windows'">10.0.17763.0</TargetPlatformMinVersion>
        <SupportedOSPlatformVersion Condition="$([MSBuild]::GetTargetPlatformIdentifier('$(TargetFramework)')) == 'tizen'">6.5</SupportedOSPlatformVersion>
    </PropertyGroup>

    <PropertyGroup Condition="'$(Configuration)|$(TargetFramework)|$(Platform)'=='Release|net9.0-android|AnyCPU'">
      <AndroidPackageFormat>apk</AndroidPackageFormat>
    </PropertyGroup>

    <ItemGroup>
        <!-- App Icon -->
        <MauiIcon Include="Resources\AppIcon\appicon.svg" ForegroundFile="Resources\AppIcon\appiconfg.svg" Color="#512BD4" />

        <!-- Splash Screen -->
        <MauiSplashScreen Include="Resources\Splash\splash.svg" Color="#512BD4" BaseSize="128,128" />

        <!-- Images -->
        <MauiImage Include="Resources\Images\*" />
        <MauiImage Update="Resources\Images\dotnet_bot.svg" BaseSize="168,208" />

        <!-- Custom Fonts -->
        <MauiFont Include="Resources\Fonts\*" />

        <!-- Raw Assets (also remove the "Resources\Raw" prefix) -->
        <MauiAsset Include="Resources\Raw\**" LogicalName="%(RecursiveDir)%(Filename)%(Extension)" />
    </ItemGroup>

    <ItemGroup>
        <PackageReference Include="Microsoft.Maui.Controls" Version="9.0.40" />
        <PackageReference Include="Microsoft.AspNetCore.Components.WebView.Maui" Version="9.0.40" />
        <PackageReference Include="Microsoft.Extensions.Logging.Debug" Version="9.0.2" />
        <PackageReference Include="Microsoft.Maui.Essentials" Version="9.0.50" />
        <PackageReference Include="Plugin.BLE" Version="3.1.0" />
    </ItemGroup>
</Project>

```

## create4care.csproj.user
```user
﻿<?xml version="1.0" encoding="utf-8"?>
<Project ToolsVersion="Current" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <PropertyGroup>
    <IsFirstTimeProjectOpen>False</IsFirstTimeProjectOpen>
    <ActiveDebugFramework>net9.0-android</ActiveDebugFramework>
    <ActiveDebugProfile>Pixel 7 - API 35 (1) (Android 15.0 - API 35)</ActiveDebugProfile>
    <SelectedPlatformGroup>Emulator</SelectedPlatformGroup>
    <DefaultDevice>pixel_7_-_api_35_1</DefaultDevice>
  </PropertyGroup>
  <PropertyGroup Condition="'$(Configuration)|$(TargetFramework)|$(Platform)'=='Debug|net9.0-android|AnyCPU'">
    <DebuggerFlavor>ProjectDebugger</DebuggerFlavor>
  </PropertyGroup>
  <PropertyGroup Condition="'$(Configuration)|$(TargetFramework)|$(Platform)'=='Release|net9.0-android|AnyCPU'">
    <DebuggerFlavor>ProjectDebugger</DebuggerFlavor>
  </PropertyGroup>
  <ItemGroup>
    <None Update="App.xaml">
      <SubType>Designer</SubType>
    </None>
    <None Update="MainPage.xaml">
      <SubType>Designer</SubType>
    </None>
    <None Update="Platforms\Windows\App.xaml">
      <SubType>Designer</SubType>
    </None>
    <None Update="Platforms\Windows\Package.appxmanifest">
      <SubType>Designer</SubType>
    </None>
  </ItemGroup>
</Project>
```

## create4care.sln
```sln
Microsoft Visual Studio Solution File, Format Version 12.00
# Visual Studio Version 17
VisualStudioVersion = 17.5.2.0
MinimumVisualStudioVersion = 10.0.40219.1
Project("{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}") = "create4care", "create4care.csproj", "{48A4972E-2DB8-D0A8-E0D5-E4634A9C672A}"
EndProject
Global
	GlobalSection(SolutionConfigurationPlatforms) = preSolution
		Debug|Any CPU = Debug|Any CPU
		Release|Any CPU = Release|Any CPU
	EndGlobalSection
	GlobalSection(ProjectConfigurationPlatforms) = postSolution
		{48A4972E-2DB8-D0A8-E0D5-E4634A9C672A}.Debug|Any CPU.ActiveCfg = Debug|Any CPU
		{48A4972E-2DB8-D0A8-E0D5-E4634A9C672A}.Debug|Any CPU.Build.0 = Debug|Any CPU
		{48A4972E-2DB8-D0A8-E0D5-E4634A9C672A}.Release|Any CPU.ActiveCfg = Release|Any CPU
		{48A4972E-2DB8-D0A8-E0D5-E4634A9C672A}.Release|Any CPU.Build.0 = Release|Any CPU
	EndGlobalSection
	GlobalSection(SolutionProperties) = preSolution
		HideSolutionNode = FALSE
	EndGlobalSection
	GlobalSection(ExtensibilityGlobals) = postSolution
		SolutionGuid = {D6FC5695-3FFC-4BAE-A5FA-CF9767E3221B}
	EndGlobalSection
EndGlobal

```

## wwwroot/css/app.css
```css
﻿/* main */
@import url('https://fonts.googleapis.com/css2?family=Raleway:ital,wght@0,100..900;1,100..900&display=swap');

:root {
    --clr-primary: #3D85EB;
    --clr-secondary: #FFE366;
    --clr-accent: #2C71A5;
    --clr-text: #171717;
    --clr-text-tint: #898989;
    --clr-text-menu: #71717A;
    --clr-indicator: #CDCDCD;
    --clr-background: #FAFAFA;
    --clr-hamburger-menu: #0D0D0D;
    --clr-link: rgba(0, 0, 0, 0.2);
    --clr-btn-text-primary: #E8E8E8;
    --clr-btn-text-secondary: #3D85EB;
    --clr-input-background: #F4F4F5;
    --clr-input-placeholder: #71717A;

    /* --space-body: 18px; */
    --padding-body-y: 18px;
    --padding-body-x: 20px;
}

@media (prefers-color-scheme: dark) {
    :root {
        --clr-primary: #145DC2;
        --clr-secondary: #997D00;
        --clr-accent: #5A9FD3;
        --clr-text: #E8E8E8;
        --clr-text-tint: #7A7A7A;
        --clr-text-menu: #a1a1aa;
        --clr-indicator: #414141;
        --clr-background: #0D0D0D;
        --clr-hamburger-menu: #FAFAFA;
        --clr-btn-text-primary: #E8E8E8;
        --clr-btn-text-secondary: #E8E8E8;
        --clr-input-background: #27272A;
        --clr-input-placeholder: #A1A1AA;

        --clr-link: rgba(255, 255, 255, 0.2);
    }
}

* {
    margin: 0;
    padding: 0;
    -webkit-tap-highlight-color: transparent;
    /* outline: 1px red solid; */
}

html, body {
    font-family: 'Raleway', sans-serif;
    overflow: hidden;
}

body {
    background-color: var(--clr-background);
    height: 100dvh;
    display: flex;
    flex-direction: column;
}

header {
    z-index: 99;
    padding: var(--padding-body-y) var(--padding-body-x);
    background: var(--clr-background);
}

main {
    flex-grow: 1;
    padding: var(--padding-body-y) var(--padding-body-x);
}

h1, h2, h3, h4, h5, h6, p, span, label, a {
    color: var(--clr-text);
}

a {
    text-decoration: none;
}

.inp {
    border: none;
    outline: none;
    background-color: var(--clr-input-background);
    color: var(--clr-text);
    padding: 16px 12px;
    border-radius: 10px;
    font-weight: 400;
    font-size: 14px;
}

.inp::placeholder {
    color: var(--clr-input-placeholder);
}

.btn {
    border: none;
    background-color: var(--clr-primary);
    color: var(--clr-btn-text-primary);
    padding: 18px 30px;
    border-radius: 10px;
    font-weight: 600;
    font-size: 15px;
    width: 100%;
}

.btn-secondary {
    background-color: transparent;
    color: var(--clr-btn-text-secondary);
}

.loader {
    width: 35px;
    height: 80px;
    position: relative;
}

.loader:after {
    content: "";
    position: absolute;
    inset: 0 0 20px;
    border-radius: 50px 50px 10px 10px;
    padding: 1px;
    background: linear-gradient(#ff4d80 33%,#ffa104 0 66%, #01ddc7 0) content-box;
    --c:radial-gradient(farthest-side,#000 94%,#0000);
    -webkit-mask:
        linear-gradient(#0000 0 0),
        var(--c) -10px -10px,
        var(--c)  15px -14px,
        var(--c)   9px -6px,
        var(--c) -12px  9px,
        var(--c)  14px  9px,
        var(--c)  23px 27px,
        var(--c)  -8px 35px,
        var(--c)   50% 50%,
        linear-gradient(#000 0 0);
    mask:
        linear-gradient(#000 0 0),
        var(--c) -10px -10px,
        var(--c)  15px -14px,
        var(--c)   9px -6px,
        var(--c) -12px  9px,
        var(--c)  14px  9px,
        var(--c)  23px 27px,
        var(--c)  -8px 35px,
        var(--c)   50% 50%,
        linear-gradient(#0000 0 0);
    -webkit-mask-composite: destination-out;
    mask-composite: exclude,add,add,add,add,add,add,add,add;
    -webkit-mask-repeat: no-repeat;
    animation: l3 3s infinite ;
}

.loader:before {
    content: "";
    position: absolute;
    inset: 50% calc(50% - 4px) 0;
    background: #e0a267;
    border-radius: 50px;
}

@keyframes l3 {
    0%   {-webkit-mask-size: auto,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0}
    10%  {-webkit-mask-size: auto,25px 25px,0 0,0 0,0 0,0 0,0 0,0 0,0 0}
    20%  {-webkit-mask-size: auto,25px 25px,25px 25px,0 0,0 0,0 0,0 0,0 0,0 0}
    30%  {-webkit-mask-size: auto,25px 25px,25px 25px,30px 30px,0 0,0 0,0 0,0 0,0 0}
    40%  {-webkit-mask-size: auto,25px 25px,25px 25px,30px 30px,30px 30px,0 0,0 0,0 0,0 0}
    50%  {-webkit-mask-size: auto,25px 25px,25px 25px,30px 30px,30px 30px,25px 25px,0 0,0 0,0 0}
    60%  {-webkit-mask-size: auto,25px 25px,25px 25px,30px 30px,30px 30px,25px 25px,25px 25px,0 0,0 0}
    70%  {-webkit-mask-size: auto,25px 25px,25px 25px,30px 30px,30px 30px,25px 25px,25px 25px,25px 25px,0 0}
    80%,
    100% {-webkit-mask-size: auto,25px 25px,25px 25px,30px 30px,30px 30px,25px 25px,25px 25px,25px 25px,200% 200%}
}


/*#endif*/
/*h1:focus {
    outline: none;
}*/

.valid.modified:not([type=checkbox]) {
    outline: 1px solid #26b050;
}

.invalid {
    outline: 1px solid #e50000;
}

.validation-message {
    color: #e50000;
}

#blazor-error-ui {
    background: lightyellow;
    bottom: 0;
    box-shadow: 0 -1px 2px rgba(0, 0, 0, 0.2);
    display: none;
    left: 0;
    padding: 0.6rem 1.25rem 0.7rem 1.25rem;
    position: fixed;
    width: 100%;
    z-index: 1000;
}

#blazor-error-ui .dismiss {
    cursor: pointer;
    position: absolute;
    right: 0.75rem;
    top: 0.5rem;
}

.blazor-error-boundary {
    background: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTYiIGhlaWdodD0iNDkiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiIG92ZXJmbG93PSJoaWRkZW4iPjxkZWZzPjxjbGlwUGF0aCBpZD0iY2xpcDAiPjxyZWN0IHg9IjIzNSIgeT0iNTEiIHdpZHRoPSI1NiIgaGVpZ2h0PSI0OSIvPjwvY2xpcFBhdGg+PC9kZWZzPjxnIGNsaXAtcGF0aD0idXJsKCNjbGlwMCkiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0yMzUgLTUxKSI+PHBhdGggZD0iTTI2My41MDYgNTFDMjY0LjcxNyA1MSAyNjUuODEzIDUxLjQ4MzcgMjY2LjYwNiA1Mi4yNjU4TDI2Ny4wNTIgNTIuNzk4NyAyNjcuNTM5IDUzLjYyODMgMjkwLjE4NSA5Mi4xODMxIDI5MC41NDUgOTIuNzk1IDI5MC42NTYgOTIuOTk2QzI5MC44NzcgOTMuNTEzIDI5MSA5NC4wODE1IDI5MSA5NC42NzgyIDI5MSA5Ny4wNjUxIDI4OS4wMzggOTkgMjg2LjYxNyA5OUwyNDAuMzgzIDk5QzIzNy45NjMgOTkgMjM2IDk3LjA2NTEgMjM2IDk0LjY3ODIgMjM2IDk0LjM3OTkgMjM2LjAzMSA5NC4wODg2IDIzNi4wODkgOTMuODA3MkwyMzYuMzM4IDkzLjAxNjIgMjM2Ljg1OCA5Mi4xMzE0IDI1OS40NzMgNTMuNjI5NCAyNTkuOTYxIDUyLjc5ODUgMjYwLjQwNyA1Mi4yNjU4QzI2MS4yIDUxLjQ4MzcgMjYyLjI5NiA1MSAyNjMuNTA2IDUxWk0yNjMuNTg2IDY2LjAxODNDMjYwLjczNyA2Ni4wMTgzIDI1OS4zMTMgNjcuMTI0NSAyNTkuMzEzIDY5LjMzNyAyNTkuMzEzIDY5LjYxMDIgMjU5LjMzMiA2OS44NjA4IDI1OS4zNzEgNzAuMDg4N0wyNjEuNzk1IDg0LjAxNjEgMjY1LjM4IDg0LjAxNjEgMjY3LjgyMSA2OS43NDc1QzI2Ny44NiA2OS43MzA5IDI2Ny44NzkgNjkuNTg3NyAyNjcuODc5IDY5LjMxNzkgMjY3Ljg3OSA2Ny4xMTgyIDI2Ni40NDggNjYuMDE4MyAyNjMuNTg2IDY2LjAxODNaTTI2My41NzYgODYuMDU0N0MyNjEuMDQ5IDg2LjA1NDcgMjU5Ljc4NiA4Ny4zMDA1IDI1OS43ODYgODkuNzkyMSAyNTkuNzg2IDkyLjI4MzcgMjYxLjA0OSA5My41Mjk1IDI2My41NzYgOTMuNTI5NSAyNjYuMTE2IDkzLjUyOTUgMjY3LjM4NyA5Mi4yODM3IDI2Ny4zODcgODkuNzkyMSAyNjcuMzg3IDg3LjMwMDUgMjY2LjExNiA4Ni4wNTQ3IDI2My41NzYgODYuMDU0N1oiIGZpbGw9IiNGRkU1MDAiIGZpbGwtcnVsZT0iZXZlbm9kZCIvPjwvZz48L3N2Zz4=) no-repeat 1rem/1.8rem, #b32121;
    padding: 1rem 1rem 1rem 3.7rem;
    color: white;
}

.blazor-error-boundary::after {
    content: "An error has occurred."
}

.status-bar-safe-area {
    display: none;
}

@supports (-webkit-touch-callout: none) {
    .status-bar-safe-area {
        display: flex;
        position: sticky;
        top: 0;
        height: env(safe-area-inset-top);
        background-color: #f7f7f7;
        width: 100%;
        z-index: 1;
    }

    .flex-column, .navbar-brand {
        padding-left: env(safe-area-inset-left);
    }
}
```

## wwwroot/index.html
```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <!-- existing meta tags, title, links, etc. -->
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover" />
        <title>create4care</title>
        <base href="/" />

        <link rel="stylesheet" href="css/app.css" />
        <link rel="stylesheet" href="create4care.styles.css" />
        <link rel="icon" href="data:,">
        
        <!-- MediaPipe Scripts -->
        <script src="https://cdn.jsdelivr.net/npm/@mediapipe/control_utils/control_utils.js" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/@mediapipe/drawing_utils/drawing_utils.js" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/@mediapipe/pose/pose.js" crossorigin="anonymous"></script>
        
        <!-- Your custom JS for starting MediaPipe Pose -->
        <script src="js/mediapipePose.js"></script>
        <script src="js/test.js"></script>
        <script src="_framework/blazor.webview.js" autostart="false" defer></script>
    </head>
    <body id="app">
        <div class="status-bar-safe-area"></div>
        <div>Loading...</div>
        <div id="blazor-error-ui">
        An unhandled error has occurred.
        <a href="" class="reload">Reload</a>
        <a class="dismiss">🗙</a>
        </div>
    </body>
</html>

```

## wwwroot/js/mediapipePose.js
```js
// Default modelComplexity = 1
// Lightweight (0)
// Standard (1)
// Heavy (2)

window.startMediapipePose = function () {
    const videoElement = document.getElementById("videoInput");
    const canvasElement = document.getElementById("output");
    const canvasCtx = canvasElement.getContext("2d");
    const counterElem = document.getElementById("counter");
    const notificationElem = document.getElementById("notification");
    const container = document.getElementById("container");

    // New elements for loading and error states.
    const loadingElem = document.getElementById("loading");
    const errorElem = document.getElementById("error");

    // Flags and timer for screenshots and posture timer.
    // let imageSaved = false;
    let landmarkImageSaved = false;
    let correctStartTime = null;
    let correctEndTime = 3;

    // Define landmark indices (based on MediaPipe Pose's 33-landmark model).
    const LANDMARKS = {
        LEFT_EAR: 7,
        RIGHT_EAR: 8,
        LEFT_SHOULDER: 11,
        RIGHT_SHOULDER: 12,
        LEFT_HIP: 23,
        RIGHT_HIP: 24,
        LEFT_KNEE: 25,
        RIGHT_KNEE: 26,
        LEFT_ANKLE: 27,
        RIGHT_ANKLE: 28,
        LEFT_HEEL: 29,
        RIGHT_HEEL: 30,
        LEFT_FOOT_INDEX: 31,
        RIGHT_FOOT_INDEX: 32,
    };

    // --- Posture Evaluation Functions ---

    // Check neck alignment between ear center and shoulder center.
    function evaluateNeckAlignment(landmarks, angleThreshold = 10) {
        const leftEar = landmarks[LANDMARKS.LEFT_EAR];
        const rightEar = landmarks[LANDMARKS.RIGHT_EAR];
        const leftShoulder = landmarks[LANDMARKS.LEFT_SHOULDER];
        const rightShoulder = landmarks[LANDMARKS.RIGHT_SHOULDER];

        if (!leftEar || !rightEar || !leftShoulder || !rightShoulder) {
            return false;
        }
    
        const shoulderCenterX = (leftShoulder.x + rightShoulder.x) / 2;
        const shoulderCenterY = (leftShoulder.y + rightShoulder.y) / 2;
        const earCenterX = (leftEar.x + rightEar.x) / 2;
        const earCenterY = (leftEar.y + rightEar.y) / 2;
    
        const deltaX = shoulderCenterX - earCenterX;
        const deltaY = shoulderCenterY - earCenterY;
        const theta = Math.atan2(deltaX, deltaY) * (180 / Math.PI);
        return Math.abs(theta) < angleThreshold;
    }

    // Check torso alignment by comparing horizontal centers of shoulders, hips, and knees.
    function evaluateTorsoAlignment(landmarks, alignmentFactor = 0.1) {
        const leftShoulder = landmarks[LANDMARKS.LEFT_SHOULDER];
        const rightShoulder = landmarks[LANDMARKS.RIGHT_SHOULDER];
        const leftHip = landmarks[LANDMARKS.LEFT_HIP];
        const rightHip = landmarks[LANDMARKS.RIGHT_HIP];
        const leftKnee = landmarks[LANDMARKS.LEFT_KNEE];
        const rightKnee = landmarks[LANDMARKS.RIGHT_KNEE];

        if (!leftShoulder || !rightShoulder || !leftHip || !rightHip || !leftKnee || !rightKnee) {
            return false;
        }
    
        const shoulderCenterY = (leftShoulder.y + rightShoulder.y) / 2;
        const hipCenterY = (leftHip.y + rightHip.y) / 2;
        const torsoLength = Math.abs(shoulderCenterY - hipCenterY);
        const threshold = torsoLength * alignmentFactor;
    
        const shoulderCenterX = (leftShoulder.x + rightShoulder.x) / 2;
        const hipCenterX = (leftHip.x + rightHip.x) / 2;
        const kneeCenterX = (leftKnee.x + rightKnee.x) / 2;
    
        return (
            Math.abs(shoulderCenterX - hipCenterX) < threshold &&
            Math.abs(hipCenterX - kneeCenterX) < threshold
        );
    }

    // Utility to calculate the angle between three points (in degrees) at point b.
    function calculateAngle(a, b, c) {
        const baX = a.x - b.x;
        const baY = a.y - b.y;
        const bcX = c.x - b.x;
        const bcY = c.y - b.y;
        const dotProduct = baX * bcX + baY * bcY;
        const normBA = Math.sqrt(baX * baX + baY * baY);
        const normBC = Math.sqrt(bcX * bcX + bcY * bcY);
        if (normBA * normBC === 0) return 0;
        const angleRad = Math.acos(dotProduct / (normBA * normBC));
        return angleRad * (180 / Math.PI);
    }

    // Ensure both knees are bent at an acceptable angle.
    function evaluateKneeAlignment(landmarks, kneeAngleThreshold = 160) {
        const leftHip = landmarks[LANDMARKS.LEFT_HIP];
        const leftKnee = landmarks[LANDMARKS.LEFT_KNEE];
        const leftAnkle = landmarks[LANDMARKS.LEFT_ANKLE];
    
        const rightHip = landmarks[LANDMARKS.RIGHT_HIP];
        const rightKnee = landmarks[LANDMARKS.RIGHT_KNEE];
        const rightAnkle = landmarks[LANDMARKS.RIGHT_ANKLE];
    
        if (!leftHip || !leftKnee || !leftAnkle || !rightHip || !rightKnee || !rightAnkle) {
            return false;
        }

        const leftAngle = calculateAngle(leftHip, leftKnee, leftAnkle);
        const rightAngle = calculateAngle(rightHip, rightKnee, rightAnkle);
    
        return leftAngle >= kneeAngleThreshold && rightAngle >= kneeAngleThreshold;
    }

    // Check that both feet are flat by comparing heel and toe vertical positions.
    function evaluateFeetFlat(landmarks, footYDiffThreshold = 0.02) {
        const leftHeel = landmarks[LANDMARKS.LEFT_HEEL];
        const rightHeel = landmarks[LANDMARKS.RIGHT_HEEL];
        const leftToe = landmarks[LANDMARKS.LEFT_FOOT_INDEX];
        const rightToe = landmarks[LANDMARKS.RIGHT_FOOT_INDEX];

        if (!leftHeel || !rightHeel || !leftToe || !rightToe) {
            return false;
        }
    
        const leftFlat = Math.abs(leftHeel.y - leftToe.y) < footYDiffThreshold;
        const rightFlat = Math.abs(rightHeel.y - rightToe.y) < footYDiffThreshold;
        return leftFlat && rightFlat;
    }

    // Combine the checks to decide if the overall posture is correct.
    function evaluatePosture(
        landmarks,
        alignmentFactor = 0.1,
        footYDiffThreshold = 0.02,
        neckAngleThreshold = 10,
        kneeAngleThreshold = 160
    ) {
        const torsoOk = evaluateTorsoAlignment(landmarks, alignmentFactor);
        const neckOk = evaluateNeckAlignment(landmarks, neckAngleThreshold);
        const kneeOk = evaluateKneeAlignment(landmarks, kneeAngleThreshold);
        const feetOk = evaluateFeetFlat(landmarks, footYDiffThreshold);
        return torsoOk && neckOk && kneeOk && feetOk;
    }

    // --- Setup MediaPipe Pose ---
    const pose = new Pose({
        locateFile: (file) =>
            `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}`,
    });

    pose.setOptions({
        modelComplexity: 0,
        smoothLandmarks: true,
        enableSegmentation: false,
        smoothSegmentation: false,
        minDetectionConfidence: 0.5,
        minTrackingConfidence: 0.5,
    });

    pose.onResults((results) => {
        if (!results.poseLandmarks) { return; }
        canvasCtx.save();

        // Clear the canvas and draw the video frame.
        canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
        canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);

        const currentTime = performance.now() / 1000; // current time in seconds
        postureOk = evaluatePosture(results.poseLandmarks);

        if (postureOk) {
            if (!correctStartTime) {
                correctStartTime = currentTime;
            }
            const elapsed = currentTime - correctStartTime;
    
            // Update the counter element with the elapsed time.
            if (counterElem) {
                counterElem.style.visibility = "visible";
                counterElem.innerText = `${elapsed.toFixed(1)}s`;
            }
    
            // If the correct posture has been maintained for 5 seconds, trigger screenshots.
            if (elapsed >= correctEndTime) {
                // if (!imageSaved) {
                //     const link = document.createElement("a");
                //     link.download = `standing_straight_${Date.now()}.png`;
                //     link.href = canvasElement.toDataURL();
                //     link.click();
                //     imageSaved = true;
                // }
                if (!landmarkImageSaved) {
                    // Create a temporary canvas for landmark-only image.
                    const blankCanvas = document.createElement("canvas");
                    blankCanvas.width = canvasElement.width;
                    blankCanvas.height = canvasElement.height;
                    const blankCtx = blankCanvas.getContext("2d");
        
                    // The drawing functions are provided by the MediaPipe drawing_utils.
                    drawConnectors(blankCtx, results.poseLandmarks, POSE_CONNECTIONS, { color: "#FFFFFF", lineWidth: 4 });
                    drawLandmarks(blankCtx, results.poseLandmarks, { color: "#FF0000", lineWidth: 2 });

                    const link2 = document.createElement("a");
                    link2.download = `landmarks_only_${Date.now()}.png`;
                    link2.href = blankCanvas.toDataURL();
                    link2.click();
                    landmarkImageSaved = true;

                    if (counterElem) { counterElem.style.display = "none"; }
                    if (notificationElem) {
                        notificationElem.style.display = "block";
                        notificationElem.innerText = "Image is saved";
                    }
                }
            }
        } else {
            correctStartTime = null;
            if (counterElem) {
                counterElem.style.visibility = "hidden";
                counterElem.innerText = "0.0s";
            }
        }

        canvasCtx.globalAlpha = 0.1;
        canvasCtx.fillStyle = postureOk ? "green" : "none";
        canvasCtx.fillRect(0, 0, canvasElement.width, canvasElement.height);
        canvasCtx.globalAlpha = 1.0;
    
        canvasCtx.restore();
    });

    // --- Function to Adjust Canvas Based on Container Width and Height ---
    function adjustCanvas() {
        const dpr = window.devicePixelRatio || 1;
        const containerWidth = container.offsetWidth;
        const containerHeight = container.offsetHeight;
    
        const videoWidth = videoElement.videoWidth;
        const videoHeight = videoElement.videoHeight;
        if (!videoWidth || !videoHeight) return;
    
        const videoAspectRatio = videoWidth / videoHeight;
        const containerAspectRatio = containerWidth / containerHeight;
    
        let displayWidth, displayHeight;
    
        if (containerAspectRatio > videoAspectRatio) {
            // Container is wider than video: fit width, crop height
            displayWidth = containerWidth;
            displayHeight = containerWidth / videoAspectRatio;
        } else {
            // Container is taller than video: fit height, crop width
            displayHeight = containerHeight;
            displayWidth = containerHeight * videoAspectRatio;
        }
    
        canvasElement.width = displayWidth * dpr;
        canvasElement.height = displayHeight * dpr;
    
        canvasElement.style.width = displayWidth + "px";
        canvasElement.style.height = displayHeight + "px";
    
        canvasCtx.setTransform(1, 0, 0, 1, 0, 0);
        canvasCtx.scale(dpr, dpr);
    }

    // Show the loading indicator.
    if (loadingElem) {
        loadingElem.style.display = "block";
    }

    // --- Start Camera and Processing Loop ---
    // navigator.mediaDevices
    //     .getUserMedia({
    //         video: {
    //             facingMode: "environment",
    //             width: { ideal: 1920 },
    //             height: { ideal: 1080 },
    //         },
    //     })
    //     .then((stream) => {
    //         videoElement.srcObject = stream;
    //         videoElement.play();
    
    //         videoElement.onloadedmetadata = () => {
    //             adjustCanvas();
        
    //             async function processFrame() {
    //                 await pose.send({ image: videoElement });
    //                 requestAnimationFrame(processFrame);
    //             }
    //             processFrame();
    //         };
    //     })
    //     .catch((error) => {
    //         console.error("Error accessing the camera:", error);
    //     });
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({
            // video: {
            //     facingMode: "environment",
            //     width: { ideal: 1920 },
            //     height: { ideal: 1080 },
            // },
            video: true,
        })
        .then((stream) => {
            // Hide any previous error messages.
            if (errorElem) {
                errorElem.style.display = "none";
            }
            videoElement.srcObject = stream;
            videoElement.play();
    
            videoElement.onloadedmetadata = () => {
                // Hide the loading indicator when the video metadata has loaded.
                if (loadingElem) {
                    loadingElem.style.display = "none";
                }
                adjustCanvas();
        
                async function processFrame() {
                    await pose.send({ image: videoElement });
                    requestAnimationFrame(processFrame);
                }
                processFrame();
            };
        })
        .catch((error) => {
            // Hide the loading indicator and display an error message.
            if (loadingElem) {
                loadingElem.style.display = "none";
            }
            if (errorElem) {
                errorElem.style.display = "block";
                errorElem.innerText = "Error accessing the camera: " + error.message;
            }
            console.error("Error accessing the camera:", error);
        });
    } else {
        errorElem.style.display = "block";
        errorElem.innerText = "getUserMedia is not supported in this browser.";
        console.error("getUserMedia is not supported in this browser.");
    }

    window.addEventListener("resize", () => {
        adjustCanvas();
        // startMediapipePose();
    });
};

```

## wwwroot/js/test.js
```js
window.mediapipePose = function () {
    const videoElement = document.getElementById('input_video');
    const canvasElement = document.getElementById('output_canvas');
    const canvasCtx = canvasElement.getContext('2d');
    
    function onResults(results) {
        if (!results.poseLandmarks) { return; }
        
        canvasCtx.save();
        canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
        canvasCtx.drawImage(results.segmentationMask, 0, 0, canvasElement.width, canvasElement.height);
        
        // Only overwrite existing pixels.
        canvasCtx.globalCompositeOperation = 'source-in';
        canvasCtx.fillStyle = '#00FF00';
        canvasCtx.fillRect(0, 0, canvasElement.width, canvasElement.height);
        
        // Only overwrite missing pixels.
        canvasCtx.globalCompositeOperation = 'destination-atop';
        canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);
        
        canvasCtx.globalCompositeOperation = 'source-over';
        drawConnectors(canvasCtx, results.poseLandmarks, POSE_CONNECTIONS, {color: '#FFFFFF', lineWidth: 4});
        drawLandmarks(canvasCtx, results.poseLandmarks, {color: '#FF0000', lineWidth: 2});
        canvasCtx.restore();
    }
    
    const pose = new Pose({locateFile: (file) => {
        return `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}`;
    }});
    pose.setOptions({
        modelComplexity: 1,
        smoothLandmarks: true,
        enableSegmentation: true,
        smoothSegmentation: true,
        minDetectionConfidence: 0.5,
        minTrackingConfidence: 0.5
    });
    pose.onResults(onResults);
    
    const camera = new Camera(videoElement, {
        onFrame: async () => {
            await pose.send({image: videoElement});
        },
        width: 854,
        height: 480
    });
    camera.start();
}
```
