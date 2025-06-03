# Folder structure
```
C:\Users\ardit\Documents\GitHub\School\year_3\sem6\create4care_app\create4care
├── App.xaml
├── App.xaml.cs
├── Components
│   ├── Layout
│   │   └── MainLayout.razor
│   ├── Models
│   │   ├── NavMenuModels.cs
│   │   └── Slides.cs
│   ├── Pages
│   │   ├── Bluetooth.razor
│   │   ├── Home.razor
│   │   ├── Instruction.razor
│   │   ├── Measuring.razor
│   │   └── Settings.razor
│   ├── Routes.razor
│   ├── Services
│   │   └── BluetoothService.cs
│   ├── Shared
│   │   ├── Icon
│   │   │   ├── Home.razor
│   │   │   ├── IconBackgroundShape.razor
│   │   │   ├── IconBluetooth.razor
│   │   │   ├── IconCamera.razor
│   │   │   ├── IconHome.razor
│   │   │   ├── IconInfo.razor
│   │   │   ├── IconInstruction.razor
│   │   │   ├── IconLogin.razor
│   │   │   ├── IconLogout.razor
│   │   │   ├── IconMeasuring.razor
│   │   │   ├── IconPerson.razor
│   │   │   └── IconSettings.razor
│   │   └── NavMenu.razor
│   └── _Imports.razor
├── MainPage.xaml
├── MainPage.xaml.cs
├── MauiProgram.cs
├── Platforms
│   ├── Android
│   │   ├── AndroidManifest.xml
│   │   ├── CustomBlazorWebViewHandler.cs
│   │   ├── MainActivity.cs
│   │   ├── MainApplication.cs
│   │   └── Resources
│   │       └── values
│   │           └── colors.xml
│   ├── MacCatalyst
│   │   ├── AppDelegate.cs
│   │   ├── Entitlements.plist
│   │   ├── Info.plist
│   │   └── Program.cs
│   ├── Tizen
│   │   ├── Main.cs
│   │   └── tizen-manifest.xml
│   ├── Windows
│   │   ├── App.xaml
│   │   ├── App.xaml.cs
│   │   ├── Package.appxmanifest
│   │   └── app.manifest
│   └── iOS
│       ├── AppDelegate.cs
│       ├── Info.plist
│       ├── Program.cs
│       └── Resources
│           └── PrivacyInfo.xcprivacy
├── Properties
│   └── launchSettings.json
├── Resources
│   ├── AppIcon
│   │   ├── appicon.svg
│   │   └── appiconfg.svg
│   ├── Fonts
│   │   └── OpenSans-Regular.ttf
│   ├── Images
│   │   ├── dotnet_bot.svg
│   │   ├── step_1.png
│   │   ├── step_2.png
│   │   ├── step_3.png
│   │   ├── step_4.png
│   │   └── step_5.png
│   ├── Raw
│   │   └── AboutAssets.txt
│   └── Splash
│       └── splash.svg
├── create4care.csproj
├── create4care.csproj.user
└── wwwroot
    ├── css
    │   └── app.css
    └── index.html
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

## Components/Models/NavMenuModels.cs
```cs
using Microsoft.AspNetCore.Components;

namespace create4care.Components.Models;

public class NavItem
{
    public required string Name { get; set; }
    public required string Href { get; set; }
    public required RenderFragment Icon { get; set; }
}

public class MenuSection
{
    public required string Header { get; set; }
    public required List<NavItem> NavItems { get; set; }
}

public class NavMenuModel
{
    public required List<MenuSection> MenuSections { get; set; }
}
```

## Components/Models/Slides.cs
```cs
using Microsoft.AspNetCore.Components;

namespace create4care.Components.Models;

public class SlidePage
{
    public object? Icon { get; set; }
    public string? Title { get; set; }
    public string? Content { get; set; }
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

    <div id="myChartContainer">
        <canvas id="myChart"></canvas>
    </div>
</main>

<script>
    // 1) Replace Utils.months(...)
    const labels = ['Week 1','Week 2','Week 3','Week 4','Week 5','Week 6','Week 7'];

    // 2) Your data
    const data = {
        labels,
        datasets: [{
            label: 'Measurement',
            data: [130,133,137,142,145,148,150],
            fill: true,
            borderColor: 'rgb(75,192,192)',
            backgroundColor: 'rgba(75,192,192,0.2)',
            tension: 0.1
        }]
    };

    // 3) Your config
    const config = {
        type: 'line',
        data,
        options: {
            scales: {
                y: {
                    min: 130,
                    max: 150,
                    ticks: {
                    stepSize: 1,
                    callback: v => v + ' cm'
                    },
                    title: {
                    display: true,
                    text: 'Height (cm)'
                    }
                },
                x: {
                    title: {
                    display: true,
                    text: 'Week'
                    }
                }
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                    label: ctx => ctx.parsed.y + ' cm'
                    }
                }
            }
        }
    };

    // 4) Instantiate the chart
    new Chart(document.getElementById('myChart'), config);
</script>

<style>
main {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

#myChartContainer {
    height: 100%;
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
        <IconBackgroundShape />
        <div class="slider-background">
            <div class="slider-page @AnimationClass">
                @if (Pages[CurrentPageIndex].Icon is RenderFragment fragment)
                {
                    @fragment
                }
                else if (Pages[CurrentPageIndex].Icon is string imageUrl)
                {
                    <img src="@imageUrl" alt="Slide icon" style="max-height: 100%;" />
                }
            </div>
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
            @* (RenderFragment)(@<IconPerson />) *@
            Icon = "images/step_1.png",
            Title = "Monteer de MeetMaatje", 
            Content = "Lorem ipsum dolor sit amet, consectetur adipiscing elit ut aliquam, purus sit amet luctus venenatis"
        },
        new SlidePage
        {
            Icon = "images/step_2.png",
            Title = "Connect met MeetMaatje",
            Content = "Lorem ipsum dolor sit amet, consectetur adipiscing elit ut aliquam, purus sit amet luctus venenatis"
        },
        new SlidePage
        {
            Icon = "images/step_3.png",
            Title = "Kalibreer de MeetMaatje",
            Content = "Lorem ipsum dolor sit amet, consectetur adipiscing elit ut aliquam, purus sit amet luctus venenatis"
        },
        new SlidePage
        {
            Icon = "images/step_4.png",
            Title = "Controleer het postuur via een foto",
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
    padding: var(--padding-body-y) 0;
}

.slider-container > svg {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-58%, -66%);
    fill: var(--clr-primary);
    width: fit-content;
    z-index: -1;
}

.slider-background {
    align-content: center;
    flex-grow: 1;
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

<NavMenu Name="Measuring" />

<main>
    <!-- <h1>Pose Measuring</h1> -->

    <span id="loading" class="center">Loading camera...</span>
    <span id="error" class="center error" hidden></span>
    <div id="container">
        <span id="notification" class="center" hidden></span>
        <video id="videoInput" muted autoplay playsinline></video>
        <canvas id="output"></canvas>
        <button id="snapshotButton" class="btn" hidden>Take Picture</button>
    </div>
    <div id="issuePopup" class="modal" hidden>
        <div class="modal-content">
            <h2>Issues Detected</h2>
            <ul id="issueList"></ul>
            <button id="retryButton" class="btn">Retry</button>
        </div>
    </div>
</main>

<script>
(() => {
    // ---- Cached DOM & State ----
    const $ = id => document.getElementById(id);
    const video      = $('videoInput');
    const canvas     = $('output');
    const loading    = $('loading');
    const errorMsg   = $('error');
    const notify     = $('notification');
    const btn        = $('snapshotButton');
    const popup      = $('issuePopup');
    const issueList  = $('issueList');
    const retryBtn   = $('retryButton');
    let capabilities = {};
    let videoDims    = { width: 1280, height: 720 };

    // ---- Generic POST helper ----
    async function postData(url, payload) {
        try {
            const res = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            return await res.json();
        } catch (err) {
            console.error(`Error POST ${url}:`, err);
            return null;
        }
    }

    // ---- Camera Setup ----
    async function setupCamera() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: 'environment', width: 1280, height: 720 }
            });
            const track = stream.getVideoTracks()[0];
            const caps  = track.getCapabilities?.() || {};
            capabilities = caps;

            // Try max resolution
            if (caps.width?.max && caps.height?.max) {
                await track.applyConstraints({
                    width: caps.width.max,
                    height: caps.height.max
                });
                videoDims = { width: caps.width.max, height: caps.height.max };
            }

            video.srcObject = stream;
            await new Promise(r => video.onloadedmetadata = r);

            loading.hidden = true;
            adjustCanvas();
            btn.hidden = false;
        } catch (err) {
            console.error('Camera error:', err);
            loading.hidden = true;
            errorMsg.hidden = false;
            errorMsg.textContent = `Error accessing camera: ${err.message}`;
        }
    }

    // ---- Canvas Sizing ----
    function adjustCanvas() {
        const { width: vw, height: vh } = videoDims;
        const CW = container.clientWidth;
        const CH = container.clientHeight;
        const scale = Math.min(CW / vw, CH / vh);
        canvas.width  = vw;
        canvas.height = vh;
        [video, canvas].forEach(el => {
            el.style.width  = `${vw * scale}px`;
            el.style.height = `${vh * scale}px`;
        });
    }

    // ---- Snapshot Flow ----
    btn.addEventListener('click', async () => {
        if (!video.paused) {
        // Capture
        video.pause();
        btn.textContent = 'Processing...';
        notify.hidden = true;

        // Draw & encode
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, videoDims.width, videoDims.height);
        const imageBase64 = canvas.toDataURL();

        // 1) Pose detection
        const pose = await postData(
            'https://api.blokk.duckdns.org/pose_detection/',
            { image_base64: imageBase64 }
        );
        if (!pose) {
            notify.textContent = 'Pose detection failed.';
            notify.hidden = false;
            return btn.textContent = 'Retry';
        }

        // 2) Show issues
        if (pose.issues?.length) {
            issueList.innerHTML = pose.issues.map(i => `<span>- ${i}</span>`).join('');
            popup.hidden = false;
            retryBtn.onclick = reset;
            return;
        }

        // 3) Save measurement
        if (pose.landmark_image) {
            const measurement = {
                patient_id: 1,
                measured_by_user_id: 1,
                height_mm: 1,
                weight_kg: 1,
                sleep_hours: 1,
                exercise_hours: 1,
                image: pose.landmark_image
            };
            const result = await postData(
                'https://api.blokk.duckdns.org/measurements/',
                measurement
            );
            notify.textContent = result
                ? 'Measurement saved!'
                : 'Failed to save measurement.';
        } else {
            notify.textContent = 'No landmark image returned.';
        }

        notify.hidden = false;
        btn.textContent = 'Retry';

        } else {
            reset();
        }
    });

    function reset() {
        popup.hidden = true;
        video.play();
        notify.hidden = true;
        btn.textContent = 'Take Picture';
    }

    // ---- (Optional) Handle resize ----
    // let resizeTimeout;
    // window.addEventListener('resize', () => {
    //   clearTimeout(resizeTimeout);
    //   resizeTimeout = setTimeout(adjustCanvas, 200);
    // });

    // ---- Init ----
    setupCamera();
})();
</script>

<style>
.center { display: block; text-align: center; }
.error  { color: red; }
[hidden] { display: none !important; }

main {
    display: flex;
    flex-direction: column;
    gap: 20px;
    overflow: auto;
}

#container {
    position: relative;
    width: 100%;
    height: 100%;
    flex-grow: 1;
    overflow: hidden;
    border-radius: 10px;
}

#notification {
    z-index: 10;
    position: absolute;
    top: 0;
    left: 0;
    padding: 10px;
    font-size: 30px;
    text-align: center;
    text-shadow: 
        -1px -1px 0 var(--clr-text-rev),
        1px -1px 0 var(--clr-text-rev),
        -1px  1px 0 var(--clr-text-rev),
        1px  1px 0 var(--clr-text-rev);
}

video, canvas {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    border-radius: 10px;
}

canvas {
    display: none;
}

#snapshotButton {
    position: absolute;
    bottom: 0;
    left: 0;
    z-index: 10;
    margin: 10px;
    width: calc(100% - 20px);
}

.modal {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background-color: var(--clr-link);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.modal-content {
    background: var(--clr-background);
    padding: 1.5rem;
    border-radius: 8px;
    max-width: 90%;
    width: 300px;
    text-align: center;
}

.modal-content ul {
    display: flex;
    flex-direction: column;
    text-align: left;
    gap: 2px;
    margin: 1em 0;
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
    private string? apiUrl { get; set; }
    private bool isSaving = false;
    private string? feedbackMessage;

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
using Plugin.BLE;
using Plugin.BLE.Abstractions.Contracts;
using Plugin.BLE.Abstractions.EventArgs;
using System.Text;

namespace create4care.Components.Services;

public class BluetoothService
{
    readonly IAdapter _adapter;
    readonly IBluetoothLE _ble;
    IDevice? _device;
    IService? _service;
    ICharacteristic? _characteristic;

    // Convert 16-bit UUIDs to full 128-bit format.
    readonly Guid serviceUuid = Guid.Parse("0000180C-0000-1000-8000-00805F9B34FB");
    readonly Guid characteristicUuid = Guid.Parse("00002A56-0000-1000-8000-00805F9B34FB");

    // Events to notify the UI
    public event Action<string>? OnStatusChanged;
    public event Action<string>? OnDataReceived;

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

    private void Characteristic_ValueUpdated(object? sender, CharacteristicUpdatedEventArgs e)
    {
        // Convert the incoming byte array (JSON data) to a string.
        string json = Encoding.UTF8.GetString(e.Characteristic.Value);
        OnDataReceived?.Invoke(json);
    }
}

```

## Components/Shared/Icon/Home.razor
```razor
﻿<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
    <g fill="none" stroke="currentColor" stroke-width="1.5">
        <path d="M2 12.204c0-2.289 0-3.433.52-4.381c.518-.949 1.467-1.537 3.364-2.715l2-1.241C9.889 2.622 10.892 2 12 2s2.11.622 4.116 1.867l2 1.241c1.897 1.178 2.846 1.766 3.365 2.715S22 9.915 22 12.203v1.522c0 3.9 0 5.851-1.172 7.063S17.771 22 14 22h-4c-3.771 0-5.657 0-6.828-1.212S2 17.626 2 13.725z"/>
        <path stroke-linecap="round" d="M12 15v3"/>
    </g>
</svg>

```

## Components/Shared/Icon/IconBackgroundShape.razor
```razor
﻿<svg width="1118" height="486" viewBox="0 0 1118 486" fill="none" xmlns="http://www.w3.org/2000/svg">
	<path d="M933.252 75.3997C676.239 203.907 387.402 78.6779 275.109 0C67.5053 181.943 -223.14 512.882 275.109 381.096C773.358 249.311 1005.28 396.121 1058.96 486C1124.15 295.589 1190.26 -53.1076 933.252 75.3997Z" fill="currentC olor"/>
</svg>

```

## Components/Shared/Icon/IconBluetooth.razor
```razor
﻿<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
	<g fill="none">
		<path stroke="currentColor" stroke-width="1.5" d="M13.933 9.8L11 12V8c0-.872 0-1.309.276-1.447c.277-.138.626.124 1.324.647l1.333 1c.49.367.734.55.734.8s-.245.434-.734.8Zm0 6l-1.333 1c-.698.524-1.047.785-1.324.647C11 17.31 11 16.873 11 16v-4l2.933 2.2c.49.367.734.55.734.8s-.245.433-.734.8Z" /><path stroke="currentColor" stroke-width="1.5" d="M2 12c0-4.714 0-7.071 1.464-8.536C4.93 2 7.286 2 12 2s7.071 0 8.535 1.464C22 4.93 22 7.286 22 12s0 7.071-1.465 8.535C19.072 22 16.714 22 12 22s-7.071 0-8.536-1.465C2 19.072 2 16.714 2 12Z" /><path fill="currentColor" d="M8.48 8.924a.75.75 0 1 0-.96 1.152zm3 2.5l-3-2.5l-.96 1.152l3 2.5z" />
		<path fill="currentColor" d="M8.48 15.076a.75.75 0 0 1-.96-1.152zm3-2.5l-3 2.5l-.96-1.152l3-2.5z" />
	</g>
</svg>
```

## Components/Shared/Icon/IconCamera.razor
```razor
﻿<svg width="276" height="226" viewBox="0 0 276 226" fill="none" xmlns="http://www.w3.org/2000/svg">
	<path d="M48.8479 30.7533H20.6753C16.9266 30.7533 13.8909 27.7175 13.8909 23.9688V7.36417C13.8909 3.61547 16.9266 0.579712 20.6753 0.579712H48.8479C52.5966 0.579712 55.6324 3.61547 55.6324 7.36417V23.9688C55.6094 27.7175 52.5736 30.7533 48.8479 30.7533Z" fill="#90A4AE"/>
	<path d="M28.2417 33.6289H19.0424V9.71083C19.0424 7.18104 21.1123 5.11121 23.6421 5.11121C26.1718 5.11121 28.2417 7.18104 28.2417 9.71083V33.6289Z" fill="#94D1E0"/>
	<path d="M88.2206 22.7747H75.5487C73.0189 22.7747 70.9721 20.7278 70.9721 18.198V5.52605C70.9721 2.99625 72.191 1.89234 75.5487 0.949419C78.9064 0.00649542 85.0239 -0.108495 88.2206 0.949419C90.8424 1.82335 92.7973 2.99625 92.7973 5.52605V18.198C92.7973 20.7278 90.7274 22.7747 88.2206 22.7747Z" fill="#546E7A"/>
	<path d="M275.977 75.9014H0V214.212H275.977V75.9014Z" fill="#212121"/>
	<path d="M0 211.083V217.361C0 221.915 3.70269 225.618 8.25631 225.618H267.744C272.297 225.618 276 221.915 276 217.361V211.083H0Z" fill="#B0BEC5"/>
	<path d="M90.4745 33.6988H73.249C67.6374 33.6988 63.0838 29.1451 63.0838 23.5336V22.0387C63.0838 16.4272 67.6374 11.8735 73.249 11.8735H90.4745C96.086 11.8735 100.64 16.4272 100.64 22.0387V23.5336C100.663 29.1451 96.109 33.6988 90.4745 33.6988Z" fill="#90A4AE"/>
	<path d="M270.757 19.0028H9.31424C4.16266 19.0028 0 23.1655 0 28.317V78.269H275.977V24.2234C275.977 21.3256 273.632 19.0028 270.757 19.0028Z" fill="#B0BEC5"/>
	<path d="M249.506 67.4833H207.765C205.327 67.4833 203.349 65.5054 203.349 63.0676V33.975C203.349 31.5372 205.327 29.5593 207.765 29.5593H249.506C251.944 29.5593 253.922 31.5372 253.922 33.975V63.0906C253.922 65.5054 251.967 67.4833 249.506 67.4833Z" fill="#78909C"/>
	<path d="M203.349 61.9637V34.4579C203.349 31.7442 205.534 29.5593 208.248 29.5593H249.161C251.461 29.5593 252.404 30.8242 252.404 30.8242L204.936 66.2873C204.936 66.2873 203.349 65.3214 203.349 61.9637Z" fill="#757575"/>
	<path d="M244.676 36.4835H212.594V60.5626H244.676V36.4835Z" fill="#212121"/>
	<path d="M15.1327 206.921H3.90967C1.74785 206.921 0 205.174 0 203.012V97.4732C0 95.3113 1.74785 93.5635 3.90967 93.5635H15.1327C17.2946 93.5635 19.0424 95.3113 19.0424 97.4732V203.012C19.0424 205.174 17.2716 206.921 15.1327 206.921Z" fill="#616161"/>
	<path d="M272.021 206.921H260.798C258.636 206.921 256.889 205.174 256.889 203.012V97.4732C256.889 95.3113 258.636 93.5635 260.798 93.5635H272.021C274.183 93.5635 275.931 95.3113 275.931 97.4732V203.012C275.931 205.174 274.183 206.921 272.021 206.921Z" fill="#616161"/>
	<path d="M9.2912 222.492C6.76142 222.492 4.69159 220.422 4.69159 217.892V212.281H13.8908V217.892C13.8908 220.422 11.844 222.492 9.2912 222.492Z" fill="#B9E4EA"/>
	<path d="M271.055 75.0282H261.856V28.112C261.856 25.5822 263.926 23.5123 266.456 23.5123C268.985 23.5123 271.055 25.5822 271.055 28.112V75.0282Z" fill="#B9E4EA"/>
	<path d="M16.4666 75.0282H7.26741V28.112C7.26741 25.5822 9.33724 23.5123 11.867 23.5123C14.3968 23.5123 16.4666 25.5822 16.4666 28.112V75.0282Z" fill="#B9E4EA"/>
	<path d="M266.456 222.492C263.926 222.492 261.856 220.422 261.856 217.892V212.281H271.055V217.892C271.055 220.422 269.008 222.492 266.456 222.492Z" fill="#B9E4EA"/>
	<path d="M130.583 56.3998C130.077 56.3998 129.64 55.9859 129.64 55.4569V31.6539C129.64 31.1479 130.054 30.7109 130.583 30.7109H183.985C184.491 30.7109 184.928 31.1249 184.928 31.6539V55.4569C184.928 55.9629 184.514 56.3998 183.985 56.3998H130.583Z" fill="#FCEBCD"/>
	<path d="M183.755 31.8821V55.2482H130.813V31.8821H183.755ZM183.985 29.5593H130.583C129.433 29.5593 128.49 30.5022 128.49 31.6522V55.4552C128.49 56.6051 129.433 57.548 130.583 57.548H183.985C185.135 57.548 186.078 56.6051 186.078 55.4552V31.6522C186.078 30.5022 185.158 29.5593 183.985 29.5593Z" fill="#78909C"/>
	<path d="M139.23 51.9597C137.482 51.9597 136.056 50.5338 136.056 48.7859V38.3448C136.056 36.5969 137.482 35.171 139.23 35.171C140.978 35.171 142.404 36.5969 142.404 38.3448V48.7859C142.404 50.5338 140.978 51.9597 139.23 51.9597Z" fill="white"/>
	<path d="M148.223 51.9597C146.889 51.9597 145.808 50.8788 145.808 49.5449V37.5858C145.808 36.2519 146.889 35.171 148.223 35.171C149.557 35.171 150.638 36.2519 150.638 37.5858V49.5449C150.638 50.8788 149.557 51.9597 148.223 51.9597Z" fill="white"/>
	<path d="M156.134 51.959C155.145 51.959 154.363 51.1541 154.363 50.1881V36.9642C154.363 35.9753 155.168 35.1934 156.134 35.1934C157.123 35.1934 157.905 35.9983 157.905 36.9642V50.1881C157.905 51.1541 157.123 51.959 156.134 51.959Z" fill="white"/>
	<path d="M157.284 218.948C198.932 218.948 232.695 185.186 232.695 143.537C232.695 101.889 198.932 68.1265 157.284 68.1265C115.636 68.1265 81.8731 101.889 81.8731 143.537C81.8731 185.186 115.636 218.948 157.284 218.948Z" fill="#616161"/>
	<path d="M157.284 209.012C193.445 209.012 222.759 179.697 222.759 143.536C222.759 107.375 193.445 78.0602 157.284 78.0602C121.123 78.0602 91.8084 107.375 91.8084 143.536C91.8084 179.697 121.123 209.012 157.284 209.012Z" fill="#E0E0E0"/>
	<path d="M157.284 190.294C183.106 190.294 204.039 169.361 204.039 143.539C204.039 117.717 183.106 96.7836 157.284 96.7836C131.462 96.7836 110.529 117.717 110.529 143.539C110.529 169.361 131.462 190.294 157.284 190.294Z" fill="#2F7889"/>
	<path d="M157.284 203.702C190.511 203.702 217.447 176.766 217.447 143.539C217.447 110.311 190.511 83.3755 157.284 83.3755C124.057 83.3755 97.1209 110.311 97.1209 143.539C97.1209 176.766 124.057 203.702 157.284 203.702Z" fill="black"/>
	<path d="M157.284 189.395C182.611 189.395 203.142 168.863 203.142 143.536C203.142 118.21 182.611 97.6781 157.284 97.6781C131.957 97.6781 111.426 118.21 111.426 143.536C111.426 168.863 131.957 189.395 157.284 189.395Z" fill="#2F7889"/>
	<path d="M146.429 105.061C131.917 108.35 123.247 122.471 123.247 132.889C123.247 141.329 128.835 139.214 130.629 136.155C135.252 128.312 140.84 121.781 150.476 119.044C154.34 117.94 158.848 115.526 158.388 111.018C157.744 104.601 151.373 103.934 146.429 105.061Z" fill="#94D1E0"/>
	<path opacity="0.25" d="M157.284 164.008C168.588 164.008 177.752 154.844 177.752 143.54C177.752 132.235 168.588 123.071 157.284 123.071C145.98 123.071 136.816 132.235 136.816 143.54C136.816 154.844 145.98 164.008 157.284 164.008Z" fill="black"/>
</svg>

```

## Components/Shared/Icon/IconHome.razor
```razor
﻿<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
	<g fill="none" stroke="currentColor" stroke-width="1.5">
		<path d="M2 12.204c0-2.289 0-3.433.52-4.381c.518-.949 1.467-1.537 3.364-2.715l2-1.241C9.889 2.622 10.892 2 12 2s2.11.622 4.116 1.867l2 1.241c1.897 1.178 2.846 1.766 3.365 2.715S22 9.915 22 12.203v1.522c0 3.9 0 5.851-1.172 7.063S17.771 22 14 22h-4c-3.771 0-5.657 0-6.828-1.212S2 17.626 2 13.725z"/>
		<path stroke-linecap="round" d="M12 15v3"/>
	</g>
</svg>
```

## Components/Shared/Icon/IconInfo.razor
```razor
﻿<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
	<g fill="none">
		<circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.5" />
		<path stroke="currentColor" stroke-linecap="round" stroke-width="1.5" d="M12 17v-6" />
		<circle cx="1" cy="1" r="1" fill="currentColor" transform="matrix(1 0 0 -1 11 9)" />
	</g>
</svg>
```

## Components/Shared/Icon/IconInstruction.razor
```razor
﻿<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
	<g fill="none" stroke="currentColor" stroke-width="1.5">
		<path d="M16 4.002c2.175.012 3.353.109 4.121.877C21 5.758 21 7.172 21 10v6c0 2.829 0 4.243-.879 5.122C19.243 22 17.828 22 15 22H9c-2.828 0-4.243 0-5.121-.878C3 20.242 3 18.829 3 16v-6c0-2.828 0-4.242.879-5.121c.768-.768 1.946-.865 4.121-.877" /><path stroke-linecap="round" d="M10.5 14H17M7 14h.5M7 10.5h.5m-.5 7h.5m3-7H17m-6.5 7H17" />
		<path d="M8 3.5A1.5 1.5 0 0 1 9.5 2h5A1.5 1.5 0 0 1 16 3.5v1A1.5 1.5 0 0 1 14.5 6h-5A1.5 1.5 0 0 1 8 4.5z" />
	</g>
</svg>
```

## Components/Shared/Icon/IconLogin.razor
```razor
﻿<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
	<g fill="none" stroke="currentColor" stroke-linecap="round" stroke-width="1.2">
		<path d="M12 20a8 8 0 1 0 0-16"/>
		<path stroke-linejoin="round" d="M4 12h10m0 0l-3-3m3 3l-3 3"/>
	</g>
</svg>
```

## Components/Shared/Icon/IconLogout.razor
```razor
﻿<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
	<g fill="none" stroke="currentColor" stroke-width="1.2">
		<circle cx="12" cy="12" r="10"/>
		<path stroke-linecap="round" d="M15 12H9"/>
	</g>
</svg>
```

## Components/Shared/Icon/IconMeasuring.razor
```razor
﻿<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
	<g fill="none">
		<path stroke="currentColor" stroke-width="1.5" d="M14 4a2 2 0 1 1-4 0a2 2 0 0 1 4 0Z" />
		<path fill="currentColor" d="m6.048 10.849l.237-.712zm2.175.725l-.237.712zm.794 1.682l-.7-.27zM7.77 16.498l.7.269zm10.182-5.649l-.237-.712zm-2.175.725l.237.712zm-.794 1.682l.7-.27zm1.247 3.242l-.7.269zm-5.806 1.26l.651.372zM12 15l.651-.372a.75.75 0 0 0-1.302 0zm5.147-7.103l-.158-.733zm-1.898.407l.157.733zm-6.498 0l.157-.734zm-1.898-.407l-.157.733zm6.723 9.86l-.651.372zm1.462-9.409l-.152-.734zm-6.076 0l-.152.735zm6.322 3.419l.394.638zm-.466.986l.743-.102zm-6.102-.986l-.394.638zm.466.986l.743.102zM5.81 11.56l2.175.726l.474-1.423l-2.175-.726zm2.506 1.427L7.07 16.228l1.4.539l1.247-3.242zm9.398-2.85l-2.175.726l.474 1.423l2.175-.726zm-3.432 3.388l1.247 3.242l1.4-.539l-1.247-3.241zm-3.208 4.605l1.576-2.758l-1.302-.744l-1.576 2.757zM16.99 7.164l-1.897.406l.314 1.467l1.898-.407zm-8.08.406l-1.9-.406l-.314 1.466l1.898.407zm2.44 7.802l1.576 2.758l1.302-.745l-1.576-2.757zm3.743-7.802l-.206.044l.304 1.469l.216-.046zM8.594 9.037l.216.046l.304-1.47l-.206-.043zm6.293-1.423a14.25 14.25 0 0 1-5.773 0L8.81 9.083a15.75 15.75 0 0 0 6.38 0zM9.145 19.25c.798 0 1.535-.428 1.93-1.12l-1.302-.745a.72.72 0 0 1-.628.365zm6.385-2.483a.723.723 0 0 1-.675.983v1.5a2.223 2.223 0 0 0 2.075-3.022zm.01-5.904c-.222.074-.458.147-.65.265l.788 1.277c-.01.005-.002-.001.056-.023c.061-.023.143-.05.28-.096zm.143 2.124a8 8 0 0 1-.104-.277c-.02-.059-.02-.069-.018-.059l-1.486.204c.03.223.124.452.208.67zm-.793-1.859a1.75 1.75 0 0 0-.815 1.727l1.486-.204a.25.25 0 0 1 .117-.246zm3.36-1.733a.78.78 0 0 1-.535.742l.474 1.423a2.28 2.28 0 0 0 1.561-2.165zM7.07 16.228a2.223 2.223 0 0 0 2.075 3.022v-1.5a.723.723 0 0 1-.675-.983zm.916-3.942c.137.045.219.073.28.096c.058.022.065.028.056.023l.788-1.277c-.192-.118-.428-.191-.65-.265zm1.73 1.24c.085-.22.178-.448.209-.671l-1.486-.204c.001-.01.001 0-.018.059a8 8 0 0 1-.104.277zm-1.394-1.121a.25.25 0 0 1 .117.246l1.486.204a1.75 1.75 0 0 0-.815-1.727zM4.25 9.395c0 .983.629 1.855 1.56 2.165l.475-1.423a.78.78 0 0 1-.535-.742zm1.5 0c0-.498.46-.87.946-.765l.315-1.466A2.282 2.282 0 0 0 4.25 9.395zm7.175 8.735a2.22 2.22 0 0 0 1.93 1.12v-1.5c-.26 0-.5-.14-.628-.365zm6.825-8.735a2.282 2.282 0 0 0-2.76-2.231l.314 1.466a.782.782 0 0 1 .946.765z" />
		<path stroke="currentColor" stroke-linecap="round" stroke-width="1.5" d="M19.454 14.5c1.583.796 2.546 1.848 2.546 3c0 2.485-4.477 4.5-10 4.5S2 19.985 2 17.5c0-1.152.963-2.204 2.546-3" />
	</g>
</svg>
```

## Components/Shared/Icon/IconPerson.razor
```razor
﻿<svg width="211" height="340" viewBox="0 0 211 340" fill="none" xmlns="http://www.w3.org/2000/svg">
	<path d="M33.9811 184.714C32.5011 200.324 30.9111 217.554 29.9411 243.294C25.1111 264.884 28.3611 282.724 30.1111 304.464C30.1111 304.464 29.6811 311.014 29.6811 318.064C29.6811 318.064 29.1711 323.444 30.8311 330.714H73.2711C73.2711 330.714 74.6011 323.294 67.3511 320.794C60.7911 318.534 56.5111 316.584 53.2711 314.794C48.7711 312.314 43.7611 304.464 43.7611 304.464C45.4311 271.544 51.0811 243.294 51.0811 243.294C51.0811 243.294 55.6111 222.354 61.7311 184.714H33.9911H33.9811Z" fill="#C39173" />
	<path style="mix-blend-mode:multiply" opacity="0.5" d="M31.4311 329.964H72.5911C72.7111 328.234 72.5411 323.384 67.1011 321.504C61.2311 319.474 56.7111 317.554 52.9011 315.454C48.2911 312.914 43.3311 305.194 43.1211 304.864C43.0411 304.734 43.0011 304.574 43.0011 304.424C44.6611 271.834 50.2811 243.424 50.3311 243.144C50.3811 242.924 54.8511 222.114 60.8311 185.454H34.6611C33.3211 199.594 31.6711 217.194 30.6811 243.314C30.6811 243.364 30.6811 243.404 30.6611 243.454C26.7311 261.004 28.1511 275.764 29.8011 292.874C30.1611 296.594 30.5311 300.444 30.8511 304.404C30.8511 304.444 30.8511 304.474 30.8511 304.514C30.8511 304.584 30.4211 311.124 30.4211 318.064C30.4211 318.084 30.4211 318.114 30.4211 318.134C30.4211 318.184 29.9711 323.204 31.4211 329.964H31.4311Z" fill="url(#paint0_linear_111_45)" />
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M32.8411 330.714H73.2611C73.2611 330.714 74.5911 323.294 67.3411 320.794C60.7811 318.534 56.5011 316.584 53.2611 314.794C48.7611 312.314 43.7511 304.464 43.7511 304.464C45.4211 271.544 51.0711 243.294 51.0711 243.294C51.0711 243.294 53.9911 229.784 58.3111 204.954C58.7911 198.814 59.2911 192.074 59.7911 184.824C59.7911 184.784 59.7911 184.744 59.8011 184.714H33.9711C32.7111 197.934 31.3811 212.314 30.4111 232.044C30.6211 238.644 30.7611 243.234 30.7611 243.234C30.7611 243.234 29.9111 262.974 32.2511 287.524H31.9511C31.1111 287.524 30.4511 288.244 30.5211 289.074L30.8811 293.294C30.9411 294.034 31.5611 294.604 32.3111 294.604H34.2011C34.2811 295.394 34.3511 296.184 34.4311 296.974H33.6811C33.2611 296.974 32.9311 297.344 32.9811 297.764C33.2511 299.934 33.5511 302.174 33.8811 304.504C33.8211 305.464 33.4611 311.554 33.4511 318.004C33.4011 318.614 33.0811 323.194 34.3111 329.484C33.5711 329.454 32.9311 329.984 32.8411 330.714Z" fill="#C39173" />
	</g>
	<path d="M53.4611 319.434C48.0111 316.814 44.7811 313.344 44.1911 312.674L39.6511 304.174V297.654C39.6511 297.284 39.9511 296.974 40.3311 296.974H44.8111C45.2211 296.974 45.5411 297.334 45.4811 297.744C45.0711 300.894 44.7611 303.264 44.6511 304.174L44.6311 304.294C44.6311 304.294 48.5811 310.424 52.8911 313.684C55.2511 315.124 58.9611 316.634 58.9611 316.634L53.4511 319.434H53.4611Z" fill="#D89A00" />
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M58.9711 316.644C58.9711 316.644 58.2411 316.344 57.2211 315.884L54.1511 317.284C54.1511 317.284 50.7011 315.854 46.5711 311.914L42.1411 303.824V299.654C42.1411 298.374 41.2411 297.314 40.0511 297.044C39.8211 297.154 39.6611 297.384 39.6611 297.654V304.174L44.2011 312.674C44.7911 313.344 48.0211 316.814 53.4711 319.434L58.9811 316.634L58.9711 316.644Z" fill="#D89A00" />
	</g>
	<path d="M67.741 319.624C64.431 318.484 61.571 317.374 59.021 316.254L55.0611 318.324C55.0611 318.324 49.931 316.824 45.591 312.684L40.931 304.184V299.804C40.931 298.254 39.671 296.994 38.121 296.994H28.6411C28.2211 296.994 27.8911 297.364 27.9411 297.784C28.2111 299.954 28.511 302.194 28.841 304.524C28.781 305.484 28.4211 311.574 28.4111 318.024C28.3511 318.684 27.981 323.954 29.591 331.004L29.8111 331.974H74.2911L74.4711 330.944C75.0011 328.014 74.2711 321.884 67.7311 319.624H67.741Z" fill="#D89A00" />
	<path style="mix-blend-mode:multiply" opacity="0.5" d="M30.4211 331.214H73.6711L73.741 330.804C74.231 328.094 73.551 322.414 67.491 320.324C64.291 319.224 61.521 318.154 59.051 317.074L55.141 319.114L54.8511 319.034C54.6311 318.974 49.5011 317.434 45.0711 313.214L44.991 313.134L40.1911 304.364V299.784C40.1911 298.644 39.2611 297.724 38.1311 297.724H28.701C28.991 300.014 29.281 302.194 29.591 304.404V304.484V304.564C29.521 305.694 29.1711 311.644 29.1611 318.014V318.074C29.1111 318.644 28.731 323.864 30.321 330.824L30.4111 331.214H30.4211Z" fill="url(#paint1_linear_111_45)" />
	<g style="mix-blend-mode:multiply" opacity="0.25">
		<path d="M42.151 331.964H29.801L29.581 330.994C27.971 323.944 28.351 318.674 28.401 318.014C28.401 318.014 41.011 318.634 42.151 331.964Z" fill="#D89A00" />
	</g>
	<path d="M44.6511 304.184H39.6511" stroke="#AA6400" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
	<path d="M46.3611 306.734H41.0211" stroke="#AA6400" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
	<path d="M48.4111 309.284H42.3511" stroke="#AA6400" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
	<path d="M50.4011 311.474L43.7711 311.834" stroke="#AA6400" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
	<path d="M52.9811 313.734L45.9111 314.384" stroke="#AA6400" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
	<path d="M55.7511 315.204L49.2511 316.934" stroke="#AA6400" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M67.741 319.624C64.431 318.484 61.571 317.374 59.021 316.254L55.0611 318.324C55.0611 318.324 49.931 316.824 45.591 312.684L40.931 304.184V299.804C40.931 298.254 39.671 296.994 38.121 296.994H28.6411C28.2211 296.994 27.8911 297.364 27.9411 297.784C28.2111 299.954 28.511 302.194 28.841 304.524C28.781 305.484 28.4211 311.574 28.4111 318.024C28.3511 318.684 27.981 323.954 29.591 331.004L29.8111 331.974H74.2911L74.4711 330.944C75.0011 328.014 74.2711 321.884 67.7311 319.624H67.741Z" fill="#D89A00" />
	</g>
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M32.8311 330.904V331.964H74.301L74.491 330.934C75.021 328.004 74.2911 321.874 67.7511 319.614C64.4411 318.474 61.5811 317.364 59.0311 316.244L55.0711 318.314C55.0711 318.314 49.9411 316.814 45.6011 312.674L40.9411 304.174V299.794C40.9411 298.244 39.6811 296.984 38.1311 296.984H33.6911C33.2711 296.984 32.9411 297.354 32.9911 297.774C33.2611 299.944 33.5611 302.184 33.8911 304.514C33.8311 305.474 33.471 311.564 33.461 318.014C33.411 318.624 33.091 323.204 34.321 329.494C33.521 329.454 32.8311 330.094 32.8311 330.914V330.904Z" fill="#D89A00" />
	</g>
	<path d="M28.1011 334.264H75.7311C75.9011 334.264 76.0511 334.124 76.0511 333.944V332.144C76.0511 331.354 75.4111 330.714 74.6211 330.714H39.6511L29.3811 329.484C28.5311 329.384 27.7811 330.044 27.7811 330.904V333.944C27.7811 334.114 27.9211 334.264 28.1011 334.264Z" fill="#223A39" />
	<path style="mix-blend-mode:multiply" opacity="0.7" d="M75.2911 332.144C75.2911 331.774 74.991 331.464 74.611 331.464H39.641L29.2811 330.234C29.0911 330.214 28.9011 330.274 28.7511 330.404C28.6011 330.534 28.5211 330.714 28.5211 330.914V333.514H75.2811V332.144H75.2911Z" fill="url(#paint2_linear_111_45)" />
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M28.1011 334.264H75.7311C75.9011 334.264 76.0511 334.124 76.0511 333.944V332.144C76.0511 331.354 75.4111 330.714 74.6211 330.714H39.6511L29.3811 329.484C28.5311 329.384 27.7811 330.044 27.7811 330.904V333.944C27.7811 334.114 27.9211 334.264 28.1011 334.264Z" fill="#223A39" />
	</g>
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M76.0411 333.944V332.144C76.0411 331.354 75.401 330.714 74.611 330.714H39.641L33.201 329.944C32.971 330.194 32.821 330.524 32.821 330.904V333.944C32.821 334.114 32.9611 334.264 33.1411 334.264H75.7311C75.9011 334.264 76.051 334.124 76.051 333.944H76.0411Z" fill="#223A39" />
	</g>
	<path d="M45.9211 291.064C48.1311 264.644 52.261 243.784 52.301 243.554C52.351 243.344 56.901 222.154 62.961 184.904L63.101 183.454H32.851C32.851 183.454 28.701 210.954 28.701 243.124C24.891 260.214 26.121 275.274 27.631 291.054H45.9211V291.064Z" fill="#316569" />
	<path style="mix-blend-mode:multiply" opacity="0.7" d="M28.311 290.314H45.2311C47.4611 264.164 51.5211 243.614 51.5711 243.404C51.6211 243.184 56.1611 222.064 62.2211 184.814L62.2811 184.214H33.511C32.901 188.524 29.461 214.074 29.461 243.134L29.4411 243.294C25.8511 259.414 26.731 273.574 28.321 290.314H28.311Z" fill="url(#paint3_linear_111_45)" />
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M45.9211 291.064C48.1311 264.644 52.261 243.784 52.301 243.554C52.351 243.344 56.901 222.154 62.961 184.904L63.101 183.454H32.851C32.851 183.454 28.701 210.954 28.701 243.124C24.891 260.214 26.121 275.274 27.631 291.054H45.9211V291.064Z" fill="#316569" />
	</g>
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M29.551 216.734C29.861 218.264 30.251 219.774 30.771 220.684L31.761 245.194C31.761 245.194 29.641 262.314 32.381 286.314H27.181C27.321 287.894 27.471 289.474 27.621 291.064H45.911C48.121 264.644 52.251 243.784 52.291 243.554C52.341 243.344 56.8911 222.154 62.951 184.904L63.091 183.454H32.841C32.841 183.454 30.761 197.254 29.541 216.724L29.551 216.734Z" fill="#316569" />
	</g>
	<path d="M27.5211 294.614H46.081C46.801 294.614 47.4011 294.084 47.5011 293.374L48.0611 289.154C48.1711 288.294 47.511 287.534 46.641 287.534H27.1611C26.3211 287.534 25.661 288.254 25.731 289.084L26.091 293.304C26.151 294.044 26.7711 294.614 27.5211 294.614Z" fill="#599091" />
	<path style="mix-blend-mode:multiply" opacity="0.7" d="M27.1611 288.274C26.9711 288.274 26.7911 288.354 26.6611 288.494C26.5311 288.634 26.4711 288.824 26.4811 289.014L26.8411 293.234C26.8711 293.584 27.1711 293.854 27.5211 293.854H46.081C46.421 293.854 46.7111 293.604 46.7611 293.264L47.3211 289.044C47.3511 288.844 47.2911 288.654 47.1611 288.504C47.0311 288.354 46.8511 288.274 46.6511 288.274H27.1711H27.1611Z" fill="url(#paint4_linear_111_45)" />
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M27.5211 294.614H46.081C46.801 294.614 47.4011 294.084 47.5011 293.374L48.0611 289.154C48.1711 288.294 47.511 287.534 46.641 287.534H27.1611C26.3211 287.534 25.661 288.254 25.731 289.084L26.091 293.304C26.151 294.044 26.7711 294.614 27.5211 294.614Z" fill="#599091" />
	</g>
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M47.5011 293.364L48.0611 289.144C48.1711 288.284 47.5111 287.524 46.6411 287.524H31.9511C31.1111 287.524 30.4511 288.244 30.5211 289.074L30.8811 293.294C30.9411 294.034 31.5611 294.604 32.3111 294.604H46.0711C46.7911 294.604 47.3911 294.074 47.4911 293.364H47.5011Z" fill="#599091" />
	</g>
	<path d="M51.7111 75.944V90.084L56.7011 94.044L58.9711 97.454L64.4011 106.334C66.4011 109.604 67.4711 113.354 67.5011 117.184L67.6011 130.044L65.6211 149.974C65.6211 149.974 63.0711 169.824 61.7211 184.734H33.9811C33.9811 184.734 29.4211 178.074 29.4211 171.994C29.4211 163.574 32.1811 159.044 35.5611 149.984C37.0211 140.464 36.7211 126.224 35.6211 119.014C34.3511 110.624 35.6911 102.064 40.3911 95.004L42.2611 90.114V75.974H51.7011L51.7111 75.944Z" fill="#C39173" />
	<path d="M33.9811 184.714C35.5911 199.304 34.1811 209.974 38.0911 243.294C33.2611 264.884 36.5111 282.724 38.2611 304.464C38.2611 304.464 37.8311 311.014 37.8311 318.064C37.8311 318.064 37.3211 323.444 38.9811 330.714H81.4211C81.4211 330.714 82.7511 323.294 75.5011 320.794C68.9411 318.534 64.6611 316.584 61.4211 314.794C56.9211 312.314 51.9111 304.464 51.9111 304.464C53.5811 271.544 56.9211 243.294 56.9211 243.294C56.9211 243.294 59.2511 220.234 61.7311 184.714H33.9911H33.9811Z" fill="#C39173" />
	<path style="mix-blend-mode:multiply" opacity="0.5" d="M39.5811 329.964H80.7511C80.8711 328.234 80.7011 323.384 75.2611 321.504C69.3911 319.474 64.8711 317.554 61.0611 315.454C56.4511 312.914 51.4911 305.194 51.2811 304.864L51.1511 304.664V304.424C52.8211 271.854 56.1411 243.484 56.1711 243.204C56.1911 242.984 58.5211 219.754 60.9711 184.654C62.3111 169.894 64.8511 150.054 64.8711 149.854L66.8511 129.984L66.7511 117.164C66.7211 113.474 65.6911 109.854 63.7611 106.704L58.3311 97.824L56.1411 94.544L50.9611 90.434V76.684H43.0211V90.214L41.0211 95.384C36.7011 101.864 35.0511 110.204 36.3611 118.864C37.4911 126.334 37.7411 140.654 36.3011 150.064L36.2611 150.214C35.5211 152.184 34.8311 153.904 34.1611 155.574C31.8411 161.344 30.1611 165.514 30.1611 171.964C30.1611 177.744 34.5411 184.214 34.5911 184.284L34.7011 184.434L34.7211 184.624C35.3511 190.314 35.5211 195.474 35.7211 201.454C36.0411 210.984 36.4411 222.844 38.8311 243.204V243.334L38.8211 243.454C34.8911 261.004 36.3111 275.764 37.9611 292.864C38.3211 296.584 38.6911 300.434 39.0111 304.394V304.444V304.494C39.0111 304.564 38.5811 311.104 38.5811 318.044V318.114C38.5811 318.164 38.1311 323.184 39.5811 329.944V329.964Z" fill="url(#paint5_linear_111_45)" />
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M42.2711 86.064C43.0811 85.824 44.1211 85.774 45.4011 86.254C47.3211 86.974 49.4211 88.114 51.7111 88.674V75.944H42.2711V86.064Z" fill="#C39173" />
	</g>
	<path d="M80.2611 63.6639C78.5911 60.1039 77.2211 56.1839 76.4711 53.9039V42.3439C76.4711 25.1239 62.5111 11.1639 45.2911 11.1639C28.0711 11.1639 14.1111 25.1239 14.1111 42.3439V46.7939C14.1111 61.4439 24.6211 73.9839 39.0411 76.5339C42.4211 77.1339 45.8311 77.7439 49.0211 78.3239C56.1511 84.1139 63.0011 85.0139 67.0911 84.8939C69.5811 84.8239 71.8211 83.3539 72.9111 81.1039C76.0511 74.5939 76.4811 66.3339 76.4811 66.3339L79.4311 65.5039C80.2211 65.2839 80.6211 64.4039 80.2711 63.6539L80.2611 63.6639Z" fill="#C39173" />
	<path style="mix-blend-mode:multiply" opacity="0.5" d="M45.3011 11.9639C28.5511 11.9639 14.9211 25.5939 14.9211 42.3439V46.7939C14.9211 61.0839 25.1311 73.2539 39.1911 75.7539C42.5811 76.3539 45.9811 76.9639 49.1711 77.5439C49.3011 77.5639 49.4311 77.6239 49.5311 77.7139C56.3211 83.2239 62.8111 84.2339 67.0711 84.1139C69.2711 84.0539 71.2311 82.7739 72.1911 80.7739C75.2211 74.4839 75.6811 66.3839 75.6911 66.3039C75.7111 65.9639 75.9411 65.6739 76.2711 65.5839L79.2211 64.7539C79.4311 64.6939 79.5211 64.5439 79.5611 64.4639C79.6011 64.3839 79.6511 64.2039 79.5611 64.0139C77.8411 60.3439 76.4211 56.2739 75.7411 54.1639C75.7111 54.0839 75.7011 54.0039 75.7011 53.9139V42.3539C75.7011 25.6039 62.0711 11.9739 45.3211 11.9739L45.3011 11.9639Z" fill="url(#paint6_linear_111_45)" />
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M76.4511 41.304C75.9011 24.574 62.1711 11.174 45.3011 11.174C28.4311 11.174 14.1211 25.134 14.1211 42.354V46.804C14.1211 61.454 24.6311 73.994 39.0511 76.544C42.4311 77.144 45.8411 77.754 49.0311 78.334C53.9411 82.314 58.7111 83.984 62.5411 84.604C48.2111 78.874 47.5311 55.3439 47.5311 55.3439C48.3011 57.2839 49.0511 58.374 49.6111 58.804C49.7911 58.944 50.0411 58.8439 50.0911 58.6239C51.8211 50.5339 55.5911 43.664 55.5911 43.664C54.7311 47.804 55.0011 50.754 55.1511 51.794C55.1811 51.994 55.4011 52.114 55.5911 52.024C62.0211 48.724 65.6111 37.474 65.6111 37.474C66.4411 45.284 69.9611 48.654 71.2611 49.654C71.4611 49.804 71.7511 49.664 71.7511 49.414C71.8911 38.684 73.5311 32.194 73.5311 32.194C73.5311 32.194 74.2911 36.744 76.4611 41.304H76.4511Z" fill="#C39173" />
	</g>
	<path d="M71.4811 48.1239L71.4511 48.0839C71.4511 48.0839 71.4311 48.0539 71.3811 48.0039C71.2911 47.9139 71.1511 47.7939 70.9511 47.6539C70.5711 47.3739 69.9811 47.1039 69.3511 47.0139C68.7211 46.9139 68.0411 47.0339 67.5311 47.2239C67.2711 47.2939 67.0711 47.4139 66.9211 47.4839C66.7711 47.5539 66.6911 47.5939 66.6911 47.5939L66.5911 47.6439C66.2011 47.8339 65.7411 47.6639 65.5611 47.2839C65.4011 46.9539 65.5011 46.5639 65.7711 46.3439C65.7711 46.3439 65.8611 46.2739 66.0211 46.1439C66.1811 46.0139 66.4011 45.8239 66.7211 45.6339C66.8811 45.5439 67.0411 45.4239 67.2311 45.3339C67.4211 45.2439 67.6311 45.1439 67.8511 45.0639C68.3011 44.9039 68.8011 44.7739 69.3311 44.7339C70.3811 44.6339 71.4411 44.8639 72.1711 45.1639C72.5411 45.3039 72.8411 45.4639 73.0511 45.5939C73.1511 45.6539 73.2411 45.7139 73.3211 45.7639C73.3711 45.8039 73.4011 45.8239 73.4011 45.8239C74.0311 46.3539 74.1111 47.3039 73.5811 47.9339C73.0511 48.5639 72.1011 48.6439 71.4711 48.1139L71.4811 48.1239Z" fill="#203F3F" />
	<path d="M71.0911 55.4339C71.0911 57.6739 71.4611 59.4939 70.0311 59.4939C68.6011 59.4939 67.4511 57.6739 67.4511 55.4339C67.4511 53.1939 68.6111 51.3739 70.0311 51.3739C71.4511 51.3739 71.0911 53.1939 71.0911 55.4339Z" fill="#203F3F" />
	<path d="M74.7211 70.994C74.7211 70.994 74.601 71.024 74.391 71.054C74.181 71.074 73.8811 71.144 73.5011 71.144C72.7411 71.184 71.7511 71.124 70.7611 70.894C69.7811 70.674 68.8411 70.274 68.1911 69.884C67.8611 69.684 67.6111 69.484 67.4411 69.344C67.2711 69.194 67.1711 69.094 67.1711 69.094C67.0611 68.974 67.0711 68.784 67.1911 68.674C67.2811 68.594 67.4011 68.574 67.5011 68.614H67.521C67.521 68.614 67.6211 68.664 67.8111 68.734C68.0011 68.814 68.2811 68.894 68.6011 69.004C69.2611 69.214 70.1411 69.474 71.0411 69.674C71.4911 69.784 71.9411 69.864 72.3711 69.954C72.8011 70.034 73.2011 70.104 73.5411 70.174C73.8911 70.244 74.1911 70.294 74.4011 70.334C74.6111 70.374 74.7311 70.404 74.7311 70.404C74.8911 70.444 74.9911 70.614 74.9411 70.774C74.9111 70.884 74.8211 70.964 74.7111 70.994H74.7211Z" fill="#996850" />
	<path d="M40.4211 7.06396C40.4211 7.06396 32.8211 4.81396 24.3811 8.81396C16.2611 12.664 10.4511 18.434 6.80107 34.234C5.17107 41.264 1.35107 45.884 0.311069 47.034C0.181069 47.184 0.221066 47.414 0.401066 47.494C3.41107 48.914 7.88108 48.054 7.88108 48.054C10.3311 70.694 23.7111 76.644 30.1711 78.064C36.6711 79.494 42.2711 82.444 42.2711 82.444C48.2811 74.494 47.1211 62.514 47.1211 62.514L43.5211 57.814L47.1211 53.694C47.5111 55.304 48.4911 56.264 49.0411 56.694C49.2111 56.834 49.4711 56.734 49.5111 56.524C51.2011 48.604 54.8911 41.884 54.8911 41.884C54.0511 45.934 54.3111 48.824 54.4611 49.834C54.4911 50.034 54.7111 50.154 54.8911 50.054C61.1911 46.824 64.7011 35.814 64.7011 35.814C65.5111 43.454 68.9611 46.754 70.2311 47.734C70.4311 47.884 70.7111 47.744 70.7111 47.504C70.8411 37.004 72.4511 30.654 72.4511 30.654C72.4511 30.654 74.981 45.874 84.1411 48.264C84.3611 48.324 84.5611 48.114 84.4911 47.894C83.9811 46.184 82.3311 40.284 82.3311 35.324C82.3311 24.494 77.5711 15.994 66.2411 9.90396C55.7811 4.29396 45.5211 5.44396 40.4311 7.07396L40.4211 7.06396Z" fill="#203F3F" />
	<path style="mix-blend-mode:multiply" opacity="0.7" d="M7.89108 47.314C8.05108 47.314 8.21108 47.364 8.34108 47.464C8.51108 47.584 8.62108 47.774 8.64108 47.984C11.1011 70.714 24.6411 76.084 30.3411 77.334C35.7311 78.524 40.4411 80.704 42.0511 81.494C47.0011 74.454 46.5111 64.364 46.4011 62.794L42.9311 58.274C42.7111 57.994 42.7311 57.594 42.9611 57.324L46.5611 53.204C46.7511 52.994 47.0311 52.904 47.3011 52.974C47.5711 53.044 47.7811 53.254 47.8511 53.524C48.0811 54.454 48.5311 55.134 48.9511 55.594C50.7011 48.004 54.0911 41.784 54.2311 41.524C54.4111 41.194 54.8011 41.054 55.1511 41.184C55.5011 41.314 55.7011 41.674 55.6211 42.044C54.9411 45.294 55.0011 47.754 55.1211 49.074C60.7111 45.664 63.9411 35.704 63.9711 35.594C64.0811 35.254 64.4111 35.044 64.7611 35.074C65.1111 35.114 65.3911 35.384 65.4311 35.744C66.0911 41.934 68.5511 45.154 69.9611 46.524C70.1711 36.634 71.6511 30.724 71.7111 30.474C71.8011 30.134 72.1111 29.884 72.4711 29.914C72.8211 29.924 73.1211 30.194 73.1811 30.544C73.2011 30.684 75.5911 44.404 83.5211 47.304C82.8611 44.944 81.5611 39.774 81.5611 35.334C81.5611 24.344 76.4311 16.244 65.8711 10.574C56.5411 5.56398 46.7211 5.85398 40.6411 7.79398C40.5011 7.84398 40.3411 7.84398 40.2011 7.79398C40.1311 7.77398 32.7611 5.68398 24.7011 9.50398C14.0311 14.564 10.2211 22.784 7.53108 34.414C6.04108 40.854 2.76108 45.314 1.29108 47.064C4.02108 48.024 7.70109 47.344 7.74109 47.334C7.79109 47.334 7.83109 47.324 7.88109 47.324L7.89108 47.314Z" fill="url(#paint7_linear_111_45)" />
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M82.3211 35.3139C82.3211 31.6139 81.7611 28.1839 80.5811 25.0339C69.5511 32.8139 56.4411 37.3239 42.3711 37.3239C30.1111 37.3239 18.5811 33.8939 8.52109 27.8739C7.91109 29.8139 7.34108 31.9239 6.81108 34.2339C5.18108 41.2639 1.36107 45.8839 0.321074 47.0339C0.191074 47.1839 0.231085 47.4139 0.411085 47.4939C3.42109 48.9139 7.89108 48.0539 7.89108 48.0539C10.3411 70.6939 23.7211 76.6439 30.1811 78.0639C36.6811 79.4939 42.2811 82.4439 42.2811 82.4439C48.2911 74.4939 47.1311 62.5139 47.1311 62.5139L43.5311 57.8139L47.1311 53.6939C47.5211 55.3039 48.5011 56.2639 49.0511 56.6939C49.2211 56.8339 49.4811 56.7339 49.5211 56.5239C51.2111 48.6039 54.9011 41.8839 54.9011 41.8839C54.0611 45.9339 54.3211 48.8239 54.4711 49.8339C54.5011 50.0339 54.7211 50.1539 54.9011 50.0539C61.2011 46.8239 64.7111 35.8139 64.7111 35.8139C65.5211 43.4539 68.9611 46.7539 70.2411 47.7339C70.4411 47.8839 70.7211 47.7439 70.7211 47.5039C70.8511 37.0039 72.4611 30.6539 72.4611 30.6539C72.4611 30.6539 74.9911 45.8739 84.1511 48.2639C84.3711 48.3239 84.5711 48.1139 84.5011 47.8939C83.9911 46.1839 82.3411 40.2839 82.3411 35.3239L82.3211 35.3139Z" fill="#203F3F" />
	</g>
	<g style="mix-blend-mode:overlay" opacity="0.5">
		<path d="M16.6111 25.494C16.6111 25.494 16.6311 25.4339 16.6711 25.3139C16.7011 25.1939 16.7711 25.0139 16.8711 24.7739C17.0811 24.3239 17.4311 23.6539 18.0211 22.9239C18.6311 22.1939 19.3711 21.3839 20.5011 20.5639C20.6411 20.4739 20.7311 20.394 20.9311 20.294C21.1311 20.194 21.3411 20.0839 21.5611 20.0239C21.9811 19.8739 22.5011 19.834 23.0011 19.904C24.0211 20.064 24.7811 20.6339 25.4211 21.1239C25.7211 21.3639 26.0311 21.604 26.3511 21.854C26.6611 22.084 26.9811 22.3139 27.3111 22.5539C27.9711 23.0639 28.6511 23.5939 29.3511 24.1439C30.6611 25.1639 32.1711 26.1639 33.4311 26.3039C33.7311 26.3339 34.0111 26.3439 34.2711 26.2639L34.3711 26.244H34.4211L34.4411 26.2339C34.2611 26.2839 34.4011 26.2339 34.3711 26.2539H34.3911L34.7411 26.1239C34.9011 26.0439 34.9211 26.0339 35.1011 25.9239C35.6911 25.5839 36.3511 24.9739 37.1211 24.2839C37.8911 23.5939 38.8311 22.7839 40.1711 22.2539L40.4211 22.1639L40.5511 22.1139L40.6111 22.0939L40.7811 22.0539H40.8011L41.1811 21.964C41.4511 21.924 41.7211 21.8939 42.0011 21.8939C42.2311 21.9039 42.4611 21.9239 42.6811 21.9539C43.5911 22.1039 44.3111 22.5039 44.8611 22.8739C45.9411 23.6339 46.6311 24.3339 47.1611 24.5939L47.2511 24.6439H47.2711L47.2811 24.6639C47.2311 24.6439 47.4111 24.7239 47.1711 24.6139L47.2611 24.654L47.6111 24.794L47.7811 24.8639H47.8311C47.8311 24.8639 47.9011 24.8639 47.9311 24.8939C48.1411 24.9039 48.3011 24.914 48.5011 24.854C48.7111 24.774 48.9811 24.654 49.3011 24.434C49.6311 24.204 49.9811 23.9339 50.3811 23.6139C50.7811 23.3039 51.2111 22.9539 51.7211 22.6439C51.9611 22.4839 52.2411 22.3339 52.5211 22.1939C52.6511 22.1239 52.8011 22.054 52.9511 21.994L53.1711 21.904L53.2811 21.854L53.3411 21.8339H53.3711L53.5511 21.7639C53.8111 21.7039 53.9011 21.6439 54.4911 21.5839C55.0111 21.5139 55.3411 21.5839 55.7211 21.6139C56.4411 21.7439 57.0311 21.9939 57.5511 22.2539C58.5511 22.7739 59.2811 23.364 59.9411 23.794C60.6111 24.244 61.1311 24.5339 61.6611 24.6239C62.0911 24.7039 62.4311 24.7339 62.7611 24.7839C63.1111 24.8139 63.4811 24.8639 63.8311 24.8639C66.6711 24.9839 69.0311 24.2939 70.4111 23.3939C71.1111 22.9539 71.5611 22.454 71.8611 22.104C72.1311 21.724 72.2711 21.5239 72.2711 21.5239L72.2911 21.5039C72.3411 21.4239 72.4511 21.414 72.5211 21.464C72.5811 21.504 72.6011 21.584 72.5811 21.654C72.5811 21.654 72.5011 21.9139 72.3511 22.3939C72.2511 22.6239 72.1111 22.914 71.9411 23.244C71.7311 23.554 71.4911 23.9239 71.1511 24.2739C70.5011 25.0039 69.5311 25.724 68.3011 26.294C67.0811 26.884 65.6011 27.294 63.9511 27.494C63.5411 27.554 63.1111 27.574 62.6711 27.604C62.2011 27.624 61.7311 27.6039 61.3411 27.5839H61.1811H61.1411H61.0511L60.9411 27.5539L60.5111 27.4839C60.2411 27.4239 59.9611 27.3439 59.7111 27.2539C59.2011 27.0739 58.7411 26.854 58.3111 26.634C57.4511 26.194 56.7011 25.7439 56.0411 25.4439C55.7211 25.3139 55.4311 25.234 55.2211 25.214C55.1411 25.214 54.9911 25.2139 55.0411 25.2339C55.1511 25.1839 54.7811 25.2939 54.5811 25.3639C54.5411 25.3739 54.8611 25.274 54.7211 25.324H54.7111L54.6811 25.3439L54.6311 25.3739L54.5211 25.4239C54.4511 25.4539 54.3811 25.494 54.3011 25.544C54.1611 25.634 54.0111 25.7239 53.8511 25.8439C53.5511 26.0639 53.2111 26.344 52.8511 26.654C52.4911 26.964 52.0711 27.3139 51.5911 27.6739C51.0911 28.0339 50.4911 28.404 49.7411 28.654C48.9811 28.904 48.1111 28.9539 47.3211 28.8439C47.1111 28.8039 46.8911 28.7539 46.6811 28.6939L46.3611 28.604L46.1811 28.5339L45.8211 28.3939L45.7311 28.3639C45.4811 28.2539 45.6411 28.324 45.5811 28.294L45.5511 28.2739L45.4911 28.244L45.2411 28.1139C43.9811 27.3739 43.2611 26.554 42.6511 26.154C42.3611 25.944 42.1511 25.8639 42.0511 25.8439C42.0211 25.8439 42.0011 25.8439 41.9711 25.8339C41.9911 25.8339 42.0111 25.8339 42.0211 25.8139L41.6511 25.8939H41.6311C41.6311 25.8939 41.8811 25.8339 41.7511 25.8639H41.7211L41.6711 25.8939L41.5611 25.934C40.9911 26.134 40.3211 26.6239 39.5611 27.2239C38.7911 27.8239 37.9611 28.564 36.8011 29.154C36.5611 29.294 36.1111 29.4639 35.8211 29.5639L35.4711 29.6639L35.3311 29.7039H35.2611L35.1311 29.7339L34.8711 29.7739C34.1711 29.9039 33.4711 29.8439 32.8311 29.7239C31.5411 29.4539 30.5611 28.8539 29.7011 28.2639C28.8511 27.6639 28.1211 27.0239 27.4611 26.3939C26.8011 25.7839 26.1911 25.134 25.6511 24.604C25.3411 24.314 25.0411 24.0239 24.7411 23.7339C24.4611 23.4439 24.1911 23.1639 23.9211 22.8939C23.4111 22.3839 22.9711 21.9939 22.6111 21.8739C22.4211 21.8139 22.2411 21.7739 22.0311 21.8139C21.9211 21.8139 21.8411 21.8539 21.7411 21.8739C21.6411 21.8939 21.4611 21.994 21.3311 22.044C20.3511 22.544 19.4111 23.144 18.7711 23.684C18.1111 24.224 17.6411 24.7239 17.3611 25.0939C17.0911 25.4439 16.9511 25.684 16.9511 25.684C16.9011 25.764 16.8011 25.794 16.7211 25.744C16.6511 25.704 16.6211 25.624 16.6411 25.544L16.6111 25.494Z" fill="white" />
	</g>
	<path d="M47.1211 53.694C47.1211 53.694 45.8911 50.574 42.9011 50.994C40.1111 51.384 38.2411 54.454 39.6511 58.894C41.0611 63.334 45.3211 64.654 47.1311 62.504V53.684L47.1211 53.694Z" fill="#C39173" />
	<path d="M46.001 59.394C46.001 59.394 46.0111 59.224 46.0111 58.884C46.0111 58.554 45.9911 58.074 45.9211 57.514C45.8411 56.954 45.7011 56.304 45.4111 55.694C45.1311 55.084 44.6511 54.554 44.0111 54.344C43.6411 54.214 43.3311 54.164 42.9711 54.174C42.6311 54.194 42.3011 54.274 42.0111 54.424C41.4211 54.724 41.0011 55.264 40.7311 55.754C40.4511 56.254 40.311 56.714 40.251 57.034C40.181 57.364 40.1911 57.544 40.1911 57.544C40.1911 57.664 40.0911 57.774 39.9711 57.774C39.8511 57.774 39.751 57.684 39.741 57.564V57.544C39.741 57.544 39.6711 56.654 40.2211 55.484C40.5011 54.914 40.9311 54.254 41.6711 53.804C42.0311 53.584 42.4711 53.434 42.9211 53.394C43.3611 53.344 43.851 53.414 44.251 53.524C45.181 53.754 45.9011 54.494 46.2911 55.224C46.7011 55.954 46.901 56.694 47.031 57.314C47.161 57.944 47.2111 58.464 47.2311 58.834C47.2511 59.204 47.251 59.434 47.251 59.434C47.251 59.794 46.961 60.074 46.621 60.064C46.271 60.064 46.001 59.774 46.001 59.434C46.001 59.424 46.001 59.404 46.001 59.394Z" fill="#996850" />
	<path style="mix-blend-mode:multiply" opacity="0.5" d="M47.1211 53.694V62.514C46.6011 62.994 45.0911 62.874 44.2511 62.704C42.9611 62.444 41.1711 61.234 40.3611 58.674C39.6911 56.544 39.7811 54.644 40.6211 53.304C41.1711 52.434 42.0111 51.874 43.0011 51.744C43.1511 51.724 43.2911 51.714 43.4311 51.714C45.2311 51.714 46.8911 53.224 47.1211 53.704V53.694Z" fill="url(#paint8_linear_111_45)" />
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M43.3311 53.374C41.8711 52.624 40.5611 53.064 39.5911 53.724C40.2011 52.184 41.4211 51.204 42.9111 50.994C45.9011 50.574 47.1311 53.694 47.1311 53.694V62.514C46.9811 62.684 46.8211 62.834 46.6411 62.964C45.6011 60.204 44.7211 56.384 44.3711 54.754C44.2411 54.164 43.8711 53.654 43.3311 53.384V53.374Z" fill="#C39173" />
	</g>
	<path d="M58.1611 243.414C58.1811 243.184 60.5211 219.924 62.9711 184.824C64.3111 170.114 66.9311 149.444 66.9311 149.444H34.3811C34.3811 149.504 32.9711 153.214 32.3211 154.824C29.9211 160.804 28.1811 165.124 28.1811 171.964C28.1811 177.724 31.7811 185.144 31.7811 185.144C32.3711 190.644 33.9511 243.224 33.9511 243.224C33.9511 243.224 33.0211 264.894 35.7911 291.064H53.9511C55.6911 264.584 58.1411 243.674 58.1711 243.414H58.1611Z" fill="#316569" />
	<path style="mix-blend-mode:multiply" opacity="0.7" d="M36.4611 290.314H53.2511C54.9511 264.634 57.3211 244.204 57.4211 243.334C57.4611 242.974 59.8011 219.594 62.2311 184.764C63.4011 171.874 65.5811 154.224 66.0911 150.184H34.9111C34.4111 151.564 33.1911 154.674 33.0211 155.094C30.6511 160.994 28.9311 165.264 28.9311 171.954C28.9311 177.474 32.4211 184.734 32.4511 184.804L32.5111 184.924V185.054C33.1111 190.524 34.6311 241.044 34.6911 243.194V243.224V243.254C34.6911 243.464 33.8111 264.794 36.4611 290.304V290.314Z" fill="url(#paint9_linear_111_45)" />
	<path d="M35.4811 294.614H54.0411C54.7611 294.614 55.3611 294.084 55.4611 293.374L56.0211 289.154C56.1311 288.294 55.4711 287.534 54.6011 287.534H35.1211C34.2811 287.534 33.6211 288.254 33.6911 289.084L34.0511 293.304C34.1111 294.044 34.7311 294.614 35.4811 294.614Z" fill="#599091" />
	<path style="mix-blend-mode:multiply" opacity="0.7" d="M35.1211 288.274C34.9311 288.274 34.7511 288.354 34.6211 288.494C34.4911 288.634 34.4311 288.824 34.4411 289.014L34.8011 293.234C34.8311 293.584 35.1311 293.854 35.4811 293.854H54.0411C54.3811 293.854 54.6711 293.604 54.7211 293.264L55.2811 289.044C55.3111 288.844 55.2511 288.654 55.1211 288.504C54.9911 288.354 54.8111 288.274 54.6111 288.274H35.1311H35.1211Z" fill="url(#paint10_linear_111_45)" />
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M32.3111 154.834C29.9111 160.814 28.1711 165.134 28.1711 171.974C28.1711 177.734 31.7711 185.154 31.7711 185.154C32.0911 188.144 32.7111 205.064 33.2011 219.874C33.3411 219.324 33.3611 218.844 33.3611 218.844C33.3611 218.844 33.9311 222.964 35.1611 222.844C36.8411 222.694 37.4211 218.944 38.3111 214.464C39.0311 210.844 39.7111 206.114 39.7111 206.114C39.7111 206.114 40.9211 211.744 41.5211 213.784C42.7111 217.804 43.4811 219.764 44.5511 219.714C45.9011 219.664 45.9311 216.404 45.6011 212.814C45.2411 208.854 44.3611 205.644 43.2111 200.514C43.2111 200.514 47.8211 207.964 51.8211 206.304C53.3911 205.654 50.2111 202.374 48.5711 198.774C46.9211 195.174 43.0311 191.114 39.7911 188.884C39.7911 188.884 40.1711 184.614 40.9811 178.944C43.9511 179.354 47.2811 179.684 50.3811 179.684C54.9111 179.684 60.0311 178.274 63.7311 176.994C65.1111 163.724 66.9211 149.434 66.9211 149.434H34.3711C34.3711 149.494 32.9611 153.204 32.3111 154.814V154.834Z" fill="#316569" />
	</g>
	<path d="M61.6711 319.434C56.2211 316.814 52.9911 313.344 52.4011 312.674L47.8611 304.174V297.654C47.8611 297.284 48.1611 296.974 48.5411 296.974H53.0211C53.4311 296.974 53.7511 297.334 53.6911 297.744C53.2811 300.894 52.9711 303.264 52.8611 304.174L52.8411 304.294C52.8411 304.294 56.7911 310.424 61.1011 313.684C63.4611 315.124 67.1711 316.634 67.1711 316.634L61.6611 319.434H61.6711Z" fill="#D89A00" />
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M67.1811 316.644C67.1811 316.644 66.4511 316.344 65.4311 315.884L62.3611 317.284C62.3611 317.284 58.9111 315.854 54.7811 311.914L50.3511 303.824V299.654C50.3511 298.374 49.4511 297.314 48.2611 297.044C48.0311 297.154 47.8711 297.384 47.8711 297.654V304.174L52.4111 312.674C53.0011 313.344 56.2311 316.814 61.6811 319.434L67.1911 316.634L67.1811 316.644Z" fill="#D89A00" />
	</g>
	<path d="M75.9511 319.624C72.6411 318.484 69.7811 317.374 67.2311 316.254L63.2711 318.324C63.2711 318.324 58.1411 316.824 53.8011 312.684L49.1411 304.184V299.804C49.1411 298.254 47.8811 296.994 46.3311 296.994H36.8511C36.4311 296.994 36.1011 297.364 36.1511 297.784C36.4211 299.954 36.7211 302.194 37.0511 304.524C36.9911 305.484 36.6311 311.574 36.6211 318.024C36.5611 318.684 36.1911 323.954 37.8011 331.004L38.0211 331.974H82.5011L82.6911 330.944C83.2211 328.014 82.4911 321.884 75.9511 319.624Z" fill="#D89A00" />
	<path style="mix-blend-mode:multiply" opacity="0.5" d="M38.6211 331.214H81.8711L81.9411 330.804C82.4311 328.094 81.7511 322.414 75.6911 320.324C72.4911 319.224 69.7211 318.154 67.2511 317.074L63.3411 319.114L63.0511 319.034C62.8311 318.974 57.7011 317.434 53.2711 313.214L53.1911 313.134L48.3911 304.364V299.784C48.3911 298.644 47.4611 297.724 46.3311 297.724H36.9011C37.1911 300.014 37.4811 302.194 37.7911 304.404V304.484V304.564C37.7211 305.694 37.3711 311.644 37.3611 318.014V318.074C37.3111 318.644 36.9311 323.864 38.5211 330.824L38.6111 331.214H38.6211Z" fill="url(#paint11_linear_111_45)" />
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M45.9911 330.494C40.1811 325.794 38.0511 316.194 38.0511 312.754C38.0511 309.314 39.7411 304.064 39.7411 304.064C37.5811 302.764 36.1811 297.824 36.1511 297.714C36.4211 299.904 36.7211 302.154 37.0511 304.514C36.9911 305.474 36.6311 311.564 36.6211 318.014C36.5611 318.674 36.1911 323.944 37.8011 330.994L38.0211 331.964H47.5811C46.4711 331.134 45.9911 330.494 45.9911 330.494Z" fill="#D89A00" />
	</g>
	<g style="mix-blend-mode:multiply" opacity="0.25">
		<path d="M50.3611 331.964H38.0111L37.7911 330.994C36.1811 323.944 36.5611 318.674 36.6111 318.014C36.6111 318.014 49.2211 318.634 50.3611 331.964Z" fill="#D89A00" />
	</g>
	<path d="M36.3111 334.264H83.9411C84.1111 334.264 84.2611 334.124 84.2611 333.944V332.144C84.2611 331.354 83.6211 330.714 82.8311 330.714H47.8611L37.5911 329.484C36.7411 329.384 35.9911 330.044 35.9911 330.904V333.944C35.9911 334.114 36.1311 334.264 36.3111 334.264Z" fill="#223A39" />
	<path style="mix-blend-mode:multiply" opacity="0.7" d="M83.5011 332.144C83.5011 331.774 83.2011 331.464 82.8211 331.464H47.8511L37.4911 330.234C37.3011 330.214 37.1111 330.274 36.9611 330.404C36.8111 330.534 36.7311 330.714 36.7311 330.914V333.514H83.4911V332.144H83.5011Z" fill="url(#paint12_linear_111_45)" />
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M36.3111 334.264C36.1411 334.264 35.9911 334.124 35.9911 333.944V330.904C35.9911 330.044 36.7411 329.384 37.5911 329.484L45.9911 330.484C45.9911 330.484 47.6511 332.694 51.9111 334.254H36.3011L36.3111 334.264Z" fill="#223A39" />
	</g>
	<path d="M52.8611 304.184H47.8611" stroke="#AA6400" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
	<path d="M54.5611 306.734H49.2211" stroke="#AA6400" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
	<path d="M56.6211 309.284H50.5511" stroke="#AA6400" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
	<path d="M58.6011 311.474L51.9711 311.834" stroke="#AA6400" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
	<path d="M61.1811 313.734L54.1211 314.384" stroke="#AA6400" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
	<path d="M63.9611 315.204L57.4611 316.934" stroke="#AA6400" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
	<path d="M68.6711 173.274C68.7811 173.224 68.851 173.114 68.851 172.984C68.851 158.344 68.571 148.534 68.601 148.314L68.351 130.094V130.054L68.251 117.154C68.221 113.184 67.111 109.304 65.041 105.924L59.601 97.0239L57.261 93.5239L55.041 91.7639C54.981 91.7139 54.911 91.694 54.841 91.684C48.861 91.434 44.241 90.5739 41.821 90.0239C41.651 89.9839 41.481 90.0739 41.411 90.2439L39.731 94.6339C35.241 101.414 32.521 110.094 33.891 119.104C34.991 126.364 25.381 164.454 25.181 171.764C25.181 171.894 25.251 172.014 25.381 172.054C27.031 172.704 38.611 177.114 49.141 177.114C59.671 177.114 67.3911 173.844 68.6711 173.284V173.274Z" fill="#EFB20C" />
	<path style="mix-blend-mode:multiply" opacity="0.5" d="M25.941 171.464C28.181 172.324 39.211 176.364 49.141 176.364C59.071 176.364 66.161 173.534 68.111 172.704C68.111 161.964 67.951 153.804 67.891 150.304C67.861 148.794 67.861 148.434 67.861 148.294L67.611 130.054V130.004L67.511 117.154C67.481 113.324 66.411 109.574 64.411 106.304L58.971 97.404L56.721 94.024L54.691 92.414C48.911 92.164 44.381 91.334 42.001 90.814L40.371 95.024C35.461 102.434 33.421 110.944 34.641 118.964C35.311 123.344 32.271 138.204 29.591 151.314C27.811 160.004 26.131 168.234 25.951 171.444L25.941 171.464Z" fill="url(#paint13_linear_111_45)" />
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M43.821 92.944C43.821 92.944 49.201 94.044 56.701 94.044" stroke="#EFB20C" stroke-width="0.5" stroke-linecap="round" stroke-linejoin="round" />
	</g>
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M43.611 164.794C44.701 160.304 45.1011 146.164 45.1011 146.164C45.1011 146.164 45.181 143.194 45.521 139.164C46.391 139.214 47.261 139.254 48.121 139.294C48.251 139.294 48.351 139.204 48.361 139.084C48.831 133.044 47.7611 124.694 50.0911 120.514C50.5911 120.094 51.5111 119.794 52.4111 120.004C52.4111 120.004 51.9711 104.394 48.5011 97.634C46.0111 92.784 41.991 92.654 40.401 92.824L39.711 94.624C35.221 101.404 32.501 110.084 33.871 119.094C34.661 124.324 29.9111 145.504 27.1111 159.694C26.8611 161.684 26.7711 163.694 26.8511 165.704V172.604C29.5311 173.584 35.1511 175.434 41.3511 176.434C41.9311 172.704 42.6811 168.604 43.6011 164.794H43.611Z" fill="#EFB20C" />
	</g>
	<path d="M39.271 186.114C39.271 186.114 40.4311 173.214 42.9811 162.714C44.0411 158.354 44.431 144.634 44.431 144.634C44.431 144.634 44.9211 125.824 48.9811 119.054C48.9811 119.054 50.4011 118.724 51.8511 119.054C51.8511 106.214 50.7311 102.044 47.7311 97.5441C44.7811 93.1241 40.4211 94.284 40.4211 94.284C35.2611 95.954 31.981 101.344 31.231 106.714C29.811 116.864 31.001 132.744 29.471 144.344L27.671 153.894C26.911 157.064 26.591 160.324 26.721 163.584L26.691 186.134C26.691 186.134 24.331 193.224 24.401 201.954C24.401 201.954 22.641 206.584 22.261 209.554C21.881 212.524 21.891 214.604 23.001 214.644C23.931 214.684 24.941 212.034 25.861 209.624C26.781 207.224 28.641 202.824 28.641 202.824C28.641 202.824 28.381 207.494 28.961 211.064C29.431 213.934 30.201 217.884 31.551 217.764C32.901 217.644 33.031 215.164 33.031 215.164C33.031 215.164 33.581 219.164 34.781 219.054C36.411 218.904 36.971 215.264 37.841 210.924C38.541 207.404 39.2011 202.824 39.2011 202.824C39.2011 202.824 40.371 208.294 40.961 210.274C42.111 214.174 42.861 216.074 43.901 216.034C45.211 215.984 45.2411 212.814 44.9211 209.334C44.5711 205.484 43.7111 202.374 42.6011 197.394C42.6011 197.394 47.071 204.624 50.961 203.014C52.491 202.384 49.401 199.204 47.801 195.704C46.201 192.204 42.421 188.264 39.271 186.104V186.114Z" fill="#C39173" />
	<path style="mix-blend-mode:multiply" opacity="0.5" d="M33.0311 214.434C33.4011 214.434 33.7211 214.714 33.7711 215.084C33.9711 216.524 34.4411 218.014 34.7811 218.314C35.6811 218.074 36.3511 214.644 36.8911 211.884L37.1011 210.794C37.7911 207.334 38.4511 202.774 38.4611 202.724C38.5111 202.364 38.8111 202.094 39.1811 202.084C39.5411 202.084 39.8611 202.324 39.9411 202.674C39.9511 202.724 41.1211 208.144 41.6811 210.064C42.7111 213.544 43.4611 215.294 43.8711 215.284C43.9011 215.264 44.6611 214.764 44.1711 209.404C43.8911 206.364 43.3011 203.824 42.4911 200.314C42.2911 199.454 42.0811 198.544 41.8611 197.564C41.7811 197.204 41.9711 196.844 42.3111 196.704C42.6511 196.564 43.0411 196.694 43.2311 197.004C44.3811 198.854 47.9211 203.394 50.6211 202.344C50.5811 201.874 49.7811 200.594 49.1811 199.654C48.4911 198.564 47.7111 197.324 47.1211 196.024C45.5411 192.564 41.7611 188.734 38.8511 186.734C38.6311 186.584 38.5011 186.314 38.5311 186.054C38.5411 185.924 39.7211 172.984 42.2611 162.544C43.2911 158.314 43.6811 144.754 43.6911 144.614C43.7111 143.844 44.2311 125.524 48.3511 118.664C48.4511 118.494 48.6211 118.364 48.8211 118.324C48.8711 118.314 49.8811 118.084 51.1111 118.184C51.0611 105.874 49.8711 102.094 47.1211 97.964C44.5211 94.064 40.7811 94.974 40.6311 95.014C37.0111 96.184 32.9011 100.304 31.9911 106.824C31.3011 111.764 31.2311 118.014 31.1611 124.644C31.0911 131.454 31.0111 138.504 30.2311 144.454L28.4211 154.044C27.6711 157.184 27.3511 160.374 27.4811 163.564L27.4511 186.144C27.4511 186.224 27.4411 186.304 27.4111 186.384C27.3911 186.454 25.0911 193.464 25.1611 201.964C25.1611 202.054 25.1411 202.154 25.1111 202.234C25.0911 202.284 23.3811 206.814 23.0111 209.664C22.5811 212.994 22.8911 213.734 23.0111 213.884C23.6011 213.464 24.6111 210.814 25.1611 209.374C26.0811 206.984 27.9411 202.594 27.9511 202.544C28.0911 202.204 28.4611 202.024 28.8111 202.104C29.1611 202.184 29.4111 202.514 29.3911 202.874C29.3911 202.924 29.1411 207.514 29.7011 210.954C30.5711 216.294 31.3111 216.954 31.5211 217.034C31.9611 216.984 32.2511 215.794 32.2911 215.134C32.3111 214.744 32.6211 214.444 33.0111 214.424C33.0211 214.424 33.0311 214.424 33.0411 214.424L33.0311 214.434Z" fill="url(#paint14_linear_111_45)" />
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M40.4311 94.284C35.2711 95.954 31.9911 101.344 31.2411 106.714C29.8211 116.864 31.0111 132.744 29.4811 144.344L27.6811 153.894C26.9211 157.064 26.6011 160.324 26.7311 163.584L26.7011 186.134C26.7011 186.134 24.3411 193.224 24.4111 201.954C24.4111 201.954 22.6511 206.584 22.2711 209.554C22.0211 211.474 21.9411 213.014 22.2111 213.874C21.6911 208.824 25.8711 201.754 25.8711 201.754C25.8711 194.244 30.1811 186.114 30.1811 186.114C30.1811 186.114 29.4311 176.914 29.4311 169.774C29.4311 162.634 35.1511 148.154 35.0311 145.284C34.9111 142.414 34.1711 138.464 34.1711 138.464C36.7811 138.864 41.1211 139.274 44.7111 139.484C45.1611 133.414 46.2811 123.534 48.9911 119.014C48.9911 119.014 50.4111 118.684 51.8611 119.014C51.8611 106.174 50.7411 102.004 47.7411 97.504C44.8011 93.084 40.4311 94.244 40.4311 94.244V94.284Z" fill="#C39173" />
	</g>
	<path d="M47.601 137.754C48.061 131.884 47.021 123.784 49.281 119.724C49.731 119.654 50.621 119.574 51.501 119.784L52.4211 120.004V119.054C52.4211 105.654 51.171 101.614 48.181 97.1239C44.971 92.3139 40.111 93.5339 40.021 93.5639C35.011 95.1839 31.201 100.304 30.321 106.604C29.611 111.634 29.051 117.944 28.981 124.614C28.981 124.614 27.261 131.704 27.061 135.314C27.061 135.424 27.131 135.514 27.231 135.544C33.491 137.174 40.691 137.634 47.371 137.954C47.491 137.954 47.601 137.874 47.611 137.744L47.601 137.754Z" fill="#EFB20C" />
	<path style="mix-blend-mode:multiply" opacity="0.5" d="M27.8311 134.934C33.7111 136.404 40.441 136.874 46.891 137.194C46.991 135.534 46.991 133.724 46.991 131.814C46.991 127.154 46.9811 122.334 48.6311 119.364L48.8111 119.044C48.8111 119.044 50.931 119.284 52.431 120.014C52.431 120.014 52.9211 102.264 47.5611 97.554C43.6411 94.114 40.4011 94.254 40.2211 94.304C35.5211 95.824 31.9111 100.704 31.0611 106.724C30.4911 110.764 29.8011 117.144 29.7211 124.644L29.701 124.814C29.681 124.884 28.1211 131.334 27.8311 134.944V134.934Z" fill="url(#paint15_linear_111_45)" />
	<path d="M128.385 202.412C128.385 202.412 134.205 207.402 136.435 208.432C138.875 209.562 145.075 209.992 145.345 208.462C145.555 207.232 142.155 206.412 138.935 205.762L134.915 202.352L128.385 202.412Z" fill="#C39173" />
	<path d="M128.385 202.412C128.385 202.412 132.905 209.772 134.395 211.732C135.885 213.692 140.395 218.762 141.745 217.412C142.845 216.312 139.775 212.072 138.035 209.532L134.915 202.352L128.385 202.412Z" fill="#C39173" />
	<path d="M128.385 202.412C128.385 202.412 132.895 209.512 135.085 210.622C137.275 211.732 143.815 214.252 144.445 212.442C144.955 210.972 140.335 208.502 137.665 206.982L134.905 202.362L128.375 202.422L128.385 202.412Z" fill="#C39173" />
	<g style="mix-blend-mode:multiply">
		<path d="M145.345 208.462C145.555 207.232 142.155 206.412 138.935 205.762L134.915 202.352L128.385 202.412C128.385 202.412 132.905 209.772 134.395 211.732C135.885 213.692 140.395 218.762 141.745 217.412C142.465 216.692 141.385 214.602 140.065 212.542C142.165 213.142 144.115 213.382 144.445 212.442C144.725 211.642 143.475 210.542 141.845 209.462C143.665 209.502 145.205 209.222 145.335 208.472L145.345 208.462Z" fill="#C39173" />
	</g>
	<path d="M146.215 94.2323L146.115 94.2623C140.955 95.9323 137.195 100.402 136.445 105.782C135.025 115.932 132.685 132.722 131.155 144.332L129.355 153.882C128.595 157.052 128.275 160.312 128.405 163.572L129.195 186.082C129.195 186.082 128.115 196.772 128.375 202.402C128.675 208.732 129.845 210.272 130.725 212.202C131.865 214.712 135.035 219.742 136.185 218.902C137.345 218.052 136.105 213.512 134.375 210.302C134.375 210.302 134.485 205.892 134.895 202.342C135.305 198.792 136.985 195.982 136.985 195.982C136.985 195.982 136.885 198.972 137.335 201.392C137.925 204.562 138.775 206.262 139.915 206.262C141.055 206.262 141.545 201.632 141.715 198.062C141.875 194.492 140.385 186.082 140.385 186.082C140.385 186.082 142.655 168.142 143.335 162.152C143.845 157.702 145.195 144.322 145.195 144.322L147.975 124.652L146.195 94.2223L146.215 94.2323Z" fill="#C39173" />
	<path style="mix-blend-mode:multiply" opacity="0.5" d="M145.525 95.2822C141.095 97.0522 137.855 101.132 137.195 105.892C135.595 117.292 133.385 133.232 131.905 144.432L130.095 154.032C129.345 157.172 129.025 160.362 129.155 163.552L129.945 186.072C129.945 186.072 129.945 186.142 129.945 186.172C129.935 186.282 128.875 196.862 129.135 202.382C129.385 207.722 130.275 209.532 131.055 211.132C131.185 211.392 131.305 211.652 131.425 211.912C132.615 214.522 134.945 217.862 135.815 218.232C136.165 217.542 135.585 214.112 133.735 210.672C133.675 210.562 133.645 210.432 133.645 210.302C133.645 210.262 133.755 205.812 134.165 202.272C134.595 198.602 136.285 195.732 136.355 195.612C136.535 195.322 136.885 195.182 137.215 195.282C137.545 195.382 137.765 195.682 137.755 196.022C137.755 196.052 137.665 198.962 138.095 201.272C138.755 204.802 139.535 205.412 139.835 205.512C140.165 205.082 140.755 203.092 140.985 198.052C141.145 194.602 139.675 186.322 139.665 186.232C139.655 186.162 139.645 186.082 139.665 186.002C139.685 185.822 141.945 168.002 142.615 162.082C143.115 157.682 144.465 144.392 144.475 144.262L147.245 124.642L145.535 95.2822H145.525Z" fill="url(#paint16_linear_111_45)" />
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M146.215 94.2323L146.115 94.2623C140.955 95.9323 137.205 100.402 136.445 105.772C135.305 113.882 133.585 126.242 132.155 136.812C134.315 137.692 137.335 138.842 140.265 139.632L135.495 174.432C135.465 174.622 135.585 174.792 135.765 174.842C136.455 175.022 138.135 175.462 139.445 175.762C139.445 175.762 139.225 192.022 139.765 206.252C139.815 206.252 139.875 206.272 139.925 206.272C141.075 206.272 141.555 201.642 141.725 198.072C141.885 194.502 140.395 186.092 140.395 186.092C140.395 186.092 142.665 168.152 143.345 162.162C143.855 157.712 145.205 144.332 145.205 144.332L147.985 124.662L146.205 94.2323H146.215Z" fill="#C39173" />
	</g>
	<path d="M145.885 93.5523C140.485 95.3023 136.495 100.062 135.705 105.672C134.525 114.122 130.515 124.182 129.145 133.812C129.115 134.022 129.235 134.232 129.435 134.302C135.565 136.572 142.525 138.362 146.395 138.482C146.625 138.482 146.815 138.322 146.855 138.092L148.735 124.762V124.692L146.905 93.2223L145.885 93.5523Z" fill="#EFB20C" />
	<path style="mix-blend-mode:multiply" opacity="0.5" d="M129.915 133.692C136.045 135.952 142.495 137.552 146.145 137.732L147.985 124.672L146.205 94.2423L146.105 94.2723C140.985 95.9323 137.185 100.452 136.435 105.792C135.855 109.942 134.625 114.402 133.315 119.112C131.985 123.912 130.615 128.872 129.905 133.692H129.915Z" fill="url(#paint17_linear_111_45)" />
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M142.895 115.572C142.895 115.572 140.145 125.352 138.585 133.682C138.585 133.682 134.295 133.872 129.275 132.982C129.235 133.262 129.185 133.542 129.145 133.822C129.115 134.032 129.235 134.242 129.435 134.312C135.565 136.582 142.525 138.372 146.395 138.492C146.625 138.492 146.815 138.332 146.855 138.102L148.735 124.772V124.702L146.905 93.2323L142.895 115.582V115.572Z" fill="#EFB20C" />
	</g>
	<path d="M172.365 81.4423V89.4423L189.075 94.2323L189.615 149.462L191.935 169.752L169.735 186.092H167.645H165.555L143.355 169.752L145.675 149.462L146.215 94.2323L162.925 89.4423V81.4423H172.365Z" fill="#C39173" />
	<path d="M165.555 186.092L163.285 243.242C164.845 261.922 163.655 282.672 161.905 304.412C161.905 304.412 162.335 310.962 162.335 318.012C162.335 318.012 162.845 323.392 161.185 330.662H127.705C127.705 330.662 127.175 323.412 133.905 320.172C140.155 317.162 143.545 313.092 143.545 313.092L148.245 304.412C148.245 304.412 145.155 280.352 143.625 269.632C142.095 258.922 143.145 243.232 143.145 243.232C143.145 243.232 138.745 193.422 143.345 169.742L157.015 179.302L165.545 186.082L165.555 186.092Z" fill="#C39173" />
	<path d="M169.735 186.092L172.005 243.242C170.445 261.922 171.635 282.672 173.385 304.412C173.385 304.412 172.955 310.962 172.955 318.012C172.955 318.012 172.445 323.392 174.105 330.662H207.585C207.585 330.662 208.115 323.412 201.385 320.172C195.135 317.162 191.745 313.092 191.745 313.092L187.045 304.412C187.045 304.412 190.135 280.352 191.665 269.632C193.195 258.922 192.145 243.232 192.145 243.232C192.145 243.232 196.545 193.422 191.945 169.742L178.275 179.302L169.745 186.082L169.735 186.092Z" fill="#C39173" />
	<path style="mix-blend-mode:multiply" opacity="0.5" d="M174.705 329.912H206.845C206.785 328.112 206.125 323.292 201.055 320.852C194.735 317.802 191.305 313.742 191.165 313.572L191.085 313.452L186.265 304.562L186.295 304.322C186.325 304.082 189.405 280.132 190.915 269.532C192.415 259.022 191.405 243.442 191.395 243.292V243.232V243.172C191.435 242.672 195.735 193.202 191.205 169.892V169.832L188.875 149.462L188.335 94.7923L171.625 90.0023V82.1923H163.675V90.0023L146.965 94.7923L146.425 149.542L144.095 169.892C139.565 193.202 143.865 242.672 143.905 243.172V243.232V243.292C143.895 243.452 142.875 259.022 144.385 269.532C145.895 280.132 148.975 304.082 149.005 304.322L149.035 304.562L144.135 313.572C143.995 313.742 140.565 317.802 134.245 320.852C129.235 323.272 128.545 328.112 128.465 329.912H160.595C162.045 323.152 161.605 318.132 161.595 318.082V318.012C161.595 311.072 161.165 304.522 161.165 304.462V304.412V304.362C163.075 280.642 164.035 261.182 162.545 243.312V243.262V243.212L164.845 185.342H170.465L172.775 243.262V243.312C171.275 261.182 172.245 280.642 174.155 304.362V304.412V304.462C174.155 304.532 173.725 311.072 173.725 318.012V318.082C173.725 318.132 173.275 323.152 174.725 329.912H174.705Z" fill="url(#paint18_linear_111_45)" />
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M172.365 81.4423H162.915V86.9223C165.495 87.4623 168.635 87.8623 172.365 87.9123V81.4423Z" fill="#C39173" />
	</g>
	<path d="M195.125 53.6422C195.125 53.6422 196.355 50.5222 199.345 50.9422C202.135 51.3322 204.005 54.4022 202.595 58.8422C201.185 63.2822 196.925 64.6022 195.115 62.4522V53.6322L195.125 53.6422Z" fill="#C39173" />
	<path d="M194.495 59.3222C194.495 59.3222 194.565 58.4522 194.935 57.2222C195.125 56.6122 195.395 55.8922 195.845 55.1922C196.075 54.8422 196.335 54.4922 196.695 54.2022C197.025 53.8922 197.465 53.6722 197.905 53.5122C198.165 53.4522 198.305 53.4122 198.545 53.3822C198.785 53.3722 199.025 53.3222 199.255 53.3622C199.715 53.3722 200.145 53.5422 200.525 53.7422C201.275 54.1922 201.735 54.8422 202.015 55.4222C202.295 56.0022 202.415 56.5322 202.475 56.9022C202.525 57.2722 202.515 57.5022 202.515 57.5022V57.5222C202.515 57.6422 202.395 57.7422 202.275 57.7322C202.155 57.7322 202.065 57.6222 202.065 57.5022C202.065 57.5022 202.065 57.3122 201.995 56.9822C201.925 56.6522 201.785 56.1822 201.505 55.6822C201.235 55.1822 200.785 54.6622 200.195 54.3522C199.895 54.2222 199.565 54.1122 199.215 54.1222C199.035 54.1022 198.885 54.1522 198.715 54.1622C198.555 54.1922 198.295 54.2722 198.165 54.3122C197.855 54.4522 197.555 54.6222 197.315 54.8722C197.065 55.1022 196.865 55.4022 196.695 55.7022C196.355 56.3022 196.155 56.9522 196.015 57.5122C195.885 58.0722 195.815 58.5522 195.775 58.8922C195.765 59.0622 195.745 59.1922 195.745 59.2722C195.745 59.3622 195.745 59.4022 195.745 59.4022C195.725 59.7422 195.425 60.0122 195.085 59.9922C194.745 59.9722 194.475 59.6722 194.495 59.3322C194.495 59.3322 194.495 59.3322 194.495 59.3222Z" fill="#996850" />
	<path style="mix-blend-mode:multiply" opacity="0.5" d="M195.875 62.1622C196.395 62.6422 197.155 62.8222 197.995 62.6522C199.285 62.3922 201.075 61.1922 201.885 58.6222C202.555 56.4922 202.465 54.5922 201.625 53.2522C201.075 52.3822 200.235 51.8222 199.245 51.6822C197.165 51.3822 196.115 53.2822 195.875 53.7922V62.1522V62.1622Z" fill="url(#paint19_linear_111_45)" />
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M198.925 53.3222C200.385 52.5722 201.695 53.0122 202.665 53.6722C202.055 52.1322 200.835 51.1522 199.345 50.9422C196.355 50.5222 195.125 53.6422 195.125 53.6422V62.4622C195.275 62.6322 195.435 62.7822 195.615 62.9122C196.655 60.1522 197.535 56.3322 197.885 54.7022C198.015 54.1122 198.385 53.6022 198.925 53.3322V53.3222Z" fill="#C39173" />
	</g>
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M195.125 53.6422V62.4622L197.605 51.1222C195.865 51.7622 195.125 53.6422 195.125 53.6422Z" fill="#C39173" />
	</g>
	<path d="M140.165 53.6422C140.165 53.6422 138.935 50.5222 135.945 50.9422C133.155 51.3322 131.285 54.4022 132.695 58.8422C134.105 63.2822 138.365 64.6022 140.175 62.4522V53.6322L140.165 53.6422Z" fill="#C39173" />
	<path d="M139.545 59.4122C139.545 59.4122 139.545 59.3622 139.545 59.2822C139.545 59.1922 139.525 59.0622 139.515 58.9022C139.475 58.5722 139.415 58.0822 139.275 57.5222C139.135 56.9622 138.935 56.3122 138.595 55.7122C138.425 55.4122 138.225 55.1122 137.975 54.8822C137.735 54.6222 137.435 54.4622 137.125 54.3222C136.995 54.2922 136.745 54.2022 136.575 54.1722C136.415 54.1722 136.255 54.1122 136.075 54.1322C135.725 54.1122 135.405 54.2322 135.095 54.3622C134.505 54.6722 134.055 55.1922 133.785 55.6922C133.505 56.1922 133.365 56.6622 133.295 56.9922C133.225 57.3222 133.225 57.5122 133.225 57.5122C133.225 57.6322 133.125 57.7422 133.005 57.7422C132.885 57.7422 132.785 57.6522 132.775 57.5322V57.5122C132.775 57.5122 132.755 57.2922 132.815 56.9122C132.875 56.5422 132.995 56.0122 133.275 55.4322C133.555 54.8522 134.015 54.2022 134.765 53.7522C135.145 53.5522 135.575 53.3822 136.035 53.3722C136.255 53.3322 136.505 53.3722 136.745 53.3922C136.985 53.4222 137.115 53.4622 137.385 53.5222C137.825 53.6822 138.265 53.9022 138.595 54.2122C138.955 54.5022 139.215 54.8622 139.445 55.2022C139.895 55.9022 140.165 56.6222 140.355 57.2322C140.725 58.4622 140.795 59.3322 140.795 59.3322C140.825 59.6822 140.565 59.9822 140.225 60.0122C139.885 60.0422 139.575 59.7822 139.545 59.4422C139.545 59.4422 139.545 59.4322 139.545 59.4222V59.4122Z" fill="#996850" />
	<path style="mix-blend-mode:multiply" opacity="0.5" d="M139.415 53.8022C139.175 53.2922 138.125 51.3922 136.045 51.6922C135.055 51.8322 134.205 52.3822 133.665 53.2622C132.825 54.6022 132.735 56.5022 133.405 58.6322C134.215 61.2022 136.005 62.4122 137.295 62.6622C138.135 62.8322 138.895 62.6522 139.415 62.1722V53.8122V53.8022Z" fill="url(#paint20_linear_111_45)" />
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M136.365 53.3222C134.905 52.5722 133.595 53.0122 132.625 53.6722C133.235 52.1322 134.455 51.1522 135.945 50.9422C138.935 50.5222 140.165 53.6422 140.165 53.6422V62.4622C140.015 62.6322 139.855 62.7822 139.675 62.9122C138.635 60.1522 137.755 56.3322 137.405 54.7022C137.275 54.1122 136.905 53.6022 136.365 53.3322V53.3222Z" fill="#C39173" />
	</g>
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M140.165 53.6422V62.4622L137.685 51.1222C139.425 51.7622 140.165 53.6422 140.165 53.6422Z" fill="#C39173" />
	</g>
	<path d="M182.755 80.6823C184.365 79.7122 185.845 78.7223 187.185 77.7523C191.945 74.3323 194.945 68.9923 195.405 63.1523L196.985 42.8523C198.315 25.7423 184.795 11.1323 167.635 11.1323C150.475 11.1323 136.955 25.7523 138.285 42.8523L139.865 63.1523C140.325 68.9923 143.325 74.3323 148.085 77.7523C149.425 78.7123 150.915 79.7122 152.515 80.6823C161.785 86.2623 173.475 86.2623 182.745 80.6823H182.755Z" fill="#C39173" />
	<path style="mix-blend-mode:multiply" opacity="0.5" d="M167.645 11.8823C159.555 11.8823 152.075 15.1523 146.585 21.0923C141.095 27.0323 138.415 34.7423 139.045 42.8023L140.625 63.1023C141.065 68.7323 143.945 73.8623 148.535 77.1523C149.985 78.1923 151.455 79.1623 152.915 80.0423C161.995 85.5123 173.285 85.5123 182.365 80.0423C183.825 79.1623 185.305 78.1923 186.745 77.1523C191.335 73.8523 194.215 68.7323 194.655 63.1023L196.235 42.8023C196.865 34.7423 194.185 27.0323 188.695 21.0923C183.205 15.1523 175.725 11.8823 167.635 11.8823H167.645Z" fill="url(#paint21_linear_111_45)" />
	<g style="mix-blend-mode:overlay" opacity="0.25">
		<path d="M188.305 75.9323C186.885 76.9523 185.315 78.0023 183.615 79.0223C173.815 84.9223 161.465 84.9223 151.655 79.0223C149.955 78.0023 148.385 76.9523 146.965 75.9323C145.215 74.6723 143.705 73.1723 142.435 71.4923C143.835 73.9323 145.745 76.0823 148.085 77.7623C149.425 78.7223 150.915 79.7223 152.515 80.6923C161.785 86.2723 173.475 86.2723 182.745 80.6923C184.355 79.7223 185.835 78.7323 187.175 77.7623C189.515 76.0823 191.425 73.9323 192.825 71.4923C191.565 73.1723 190.045 74.6823 188.295 75.9323H188.305Z" fill="white" />
	</g>
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M167.645 11.1323C150.485 11.1323 136.965 25.7523 138.295 42.8523L139.065 52.7423C139.875 50.3923 140.735 48.3523 141.435 46.8123C141.185 49.3723 141.355 51.2023 141.465 52.0223C141.505 52.3023 141.675 52.5423 141.925 52.6623C142.165 52.7923 142.455 52.7923 142.705 52.6623C147.815 50.0123 151.155 42.8123 152.515 39.3423C153.695 45.9923 156.805 49.0823 158.175 50.1523C158.425 50.3523 158.765 50.3923 159.055 50.2523C159.345 50.1123 159.535 49.8223 159.545 49.4923C159.725 41.2423 162.045 35.4323 163.125 33.1623C164.365 36.7823 168.895 47.5923 179.785 50.8223C180.055 50.9023 180.345 50.8423 180.555 50.6723C180.775 50.5023 180.895 50.2323 180.875 49.9523C180.775 48.4523 180.555 43.4923 181.425 38.4223C182.985 41.7823 187.195 49.8823 192.585 52.6723C192.825 52.7923 193.115 52.7923 193.365 52.6723C193.615 52.5423 193.785 52.3023 193.815 52.0323C193.925 51.2223 194.095 49.3823 193.845 46.8223C194.545 48.3522 195.405 50.4023 196.215 52.7423L196.985 42.8523C198.315 25.7423 184.795 11.1323 167.635 11.1323H167.645Z" fill="#C39173" />
	</g>
	<path d="M180.325 55.3822C180.325 57.6222 181.485 59.4422 182.905 59.4422C184.325 59.4422 185.485 57.6222 185.485 55.3822C185.485 53.1422 184.325 51.3221 182.905 51.3221C181.485 51.3221 180.325 53.1422 180.325 55.3822Z" fill="#203F3F" />
	<path d="M178.825 45.7722C178.825 45.7722 178.855 45.7522 178.905 45.7122C178.985 45.6622 179.075 45.5922 179.175 45.5422C179.385 45.4222 179.685 45.2622 180.055 45.1122C180.785 44.8122 181.845 44.5822 182.895 44.6822C183.415 44.7222 183.925 44.8522 184.375 45.0122C184.595 45.0922 184.805 45.2022 184.995 45.2822C185.195 45.3622 185.355 45.4922 185.505 45.5822C185.825 45.7622 186.045 45.9622 186.205 46.0922C186.365 46.2222 186.455 46.2922 186.455 46.2922C186.785 46.5622 186.845 47.0522 186.575 47.3822C186.345 47.6722 185.955 47.7522 185.635 47.5922L185.535 47.5422C185.535 47.5422 185.455 47.5022 185.305 47.4322C185.155 47.3622 184.955 47.2422 184.695 47.1722C184.195 46.9822 183.505 46.8622 182.875 46.9622C182.245 47.0422 181.665 47.3222 181.275 47.6022C181.085 47.7322 180.935 47.8622 180.845 47.9522C180.795 48.0022 180.775 48.0222 180.775 48.0322C180.775 48.0322 180.735 48.0822 180.745 48.0722C180.115 48.6022 179.165 48.5322 178.635 47.8922C178.105 47.2622 178.175 46.3122 178.815 45.7822L178.825 45.7722Z" fill="#203F3F" />
	<path d="M154.525 48.0722L154.495 48.0322C154.495 48.0322 154.475 48.0022 154.425 47.9522C154.335 47.8622 154.195 47.7422 153.995 47.6022C153.615 47.3222 153.025 47.0522 152.395 46.9622C151.765 46.8622 151.085 46.9822 150.575 47.1722C150.315 47.2422 150.115 47.3622 149.965 47.4322C149.815 47.5022 149.735 47.5422 149.735 47.5422L149.635 47.5922C149.245 47.7822 148.785 47.6122 148.605 47.2322C148.445 46.9022 148.545 46.5122 148.815 46.2922C148.815 46.2922 148.905 46.2222 149.065 46.0922C149.225 45.9622 149.445 45.7722 149.765 45.5822C149.925 45.4922 150.085 45.3722 150.275 45.2822C150.465 45.1922 150.675 45.0922 150.895 45.0122C151.345 44.8522 151.845 44.7222 152.375 44.6822C153.425 44.5822 154.485 44.8122 155.215 45.1122C155.585 45.2522 155.885 45.4122 156.095 45.5422C156.195 45.6022 156.285 45.6622 156.365 45.7122C156.415 45.7522 156.445 45.7722 156.445 45.7722C157.075 46.3022 157.155 47.2522 156.625 47.8822C156.095 48.5122 155.145 48.5922 154.515 48.0622L154.525 48.0722Z" fill="#203F3F" />
	<path d="M154.965 55.3822C154.965 57.6222 153.805 59.4422 152.385 59.4422C150.965 59.4422 149.805 57.6222 149.805 55.3822C149.805 53.1422 150.965 51.3221 152.385 51.3221C153.805 51.3221 154.965 53.1422 154.965 55.3822Z" fill="#203F3F" />
	<path d="M175.195 69.0422C175.195 69.0422 174.995 69.2222 174.625 69.4622C174.255 69.6922 173.705 70.0222 173.005 70.2922C172.305 70.5622 171.475 70.8422 170.545 71.0022C170.085 71.0922 169.605 71.1522 169.115 71.1922C168.625 71.2422 168.145 71.2622 167.615 71.2722C166.675 71.2522 165.625 71.1622 164.715 71.0022C163.795 70.8422 162.955 70.5622 162.255 70.2922C161.555 70.0222 161.015 69.6922 160.635 69.4622C160.445 69.3422 160.315 69.2322 160.215 69.1622C160.115 69.0822 160.065 69.0422 160.065 69.0422C159.935 68.9422 159.925 68.7522 160.025 68.6322C160.115 68.5222 160.265 68.4922 160.385 68.5522L160.415 68.5722C160.415 68.5722 160.465 68.5922 160.555 68.6422C160.655 68.6822 160.795 68.7522 160.975 68.8322C161.345 69.0022 161.895 69.1822 162.565 69.3822C163.235 69.5822 164.035 69.7322 164.895 69.8522C165.325 69.9222 165.775 69.9622 166.225 69.9922C166.665 70.0222 167.155 70.0222 167.635 70.0322C168.075 70.0322 168.555 70.0322 169.005 69.9922C169.465 69.9622 169.915 69.9222 170.345 69.8522C171.205 69.7222 172.005 69.5822 172.675 69.3822C173.345 69.1822 173.895 69.0022 174.265 68.8322C174.645 68.6722 174.835 68.5622 174.835 68.5622C174.975 68.4822 175.155 68.5322 175.235 68.6722C175.305 68.7922 175.275 68.9422 175.175 69.0322L175.195 69.0422Z" fill="#996850" />
	<path d="M163.445 30.6023C163.445 30.6023 166.995 44.5422 179.325 48.2022C179.545 48.2722 179.775 48.0923 179.755 47.8523C179.645 46.2123 179.405 40.6322 180.575 35.2622C180.575 35.2622 185.275 46.7022 191.595 49.9822C191.795 50.0922 192.045 49.9522 192.075 49.7222C192.225 48.6622 192.465 45.8022 191.635 41.8222C191.635 41.8222 195.235 48.3922 196.955 56.1822C197.015 56.4722 197.385 56.5522 197.555 56.3122C198.405 55.0822 200.165 52.0522 200.165 48.0122C200.165 48.0122 204.575 48.8522 207.585 47.4822C207.795 47.3822 207.855 47.1222 207.705 46.9522C206.625 45.7422 202.865 41.1522 201.255 34.1922C197.605 18.4022 192.255 11.5622 184.145 7.71224C175.705 3.71224 167.645 7.02224 167.645 7.02224C167.645 7.02224 159.585 3.71224 151.145 7.71224C143.025 11.5622 137.685 18.4022 134.035 34.1922C132.425 41.1522 128.665 45.7422 127.585 46.9522C127.435 47.1222 127.495 47.3822 127.705 47.4822C130.715 48.8522 135.125 48.0122 135.125 48.0122C135.125 52.0522 136.885 55.0922 137.735 56.3122C137.905 56.5522 138.275 56.4722 138.335 56.1822C140.055 48.3922 143.655 41.8222 143.655 41.8222C142.825 45.8022 143.065 48.6622 143.215 49.7222C143.245 49.9522 143.495 50.0822 143.695 49.9822C149.965 46.7222 153.455 35.7622 153.455 35.7622C154.255 43.2922 157.615 46.6123 158.925 47.6323C159.145 47.8022 159.455 47.6422 159.465 47.3722C159.695 36.9122 163.455 30.5922 163.455 30.5922L163.445 30.6023Z" fill="#203F3F" />
	<path style="mix-blend-mode:multiply" opacity="0.7" d="M191.645 41.0722C191.915 41.0722 192.165 41.2122 192.305 41.4622C192.445 41.7222 195.695 47.6822 197.475 55.0522C198.305 53.6322 199.425 51.1322 199.425 48.0022C199.425 47.7822 199.525 47.5622 199.695 47.4222C199.865 47.2822 200.095 47.2222 200.315 47.2622C200.355 47.2622 204.035 47.9522 206.765 46.9922C205.315 45.2622 202.015 40.7922 200.525 34.3422C196.405 16.5222 190.065 11.3322 183.825 8.37224C175.805 4.57224 168.005 7.67224 167.935 7.70224C167.755 7.77224 167.545 7.77224 167.365 7.70224C167.285 7.67224 159.495 4.57224 151.475 8.37224C145.235 11.3322 138.895 16.5222 134.765 34.3422C133.275 40.7922 129.975 45.2622 128.525 46.9922C131.255 47.9522 134.935 47.2722 134.975 47.2622C135.195 47.2222 135.425 47.2822 135.595 47.4222C135.765 47.5622 135.865 47.7722 135.865 48.0022C135.865 51.1322 136.995 53.6322 137.815 55.0522C139.595 47.6822 142.845 41.7222 142.985 41.4622C143.165 41.1322 143.555 40.9922 143.905 41.1222C144.255 41.2522 144.455 41.6122 144.375 41.9822C143.695 45.2422 143.755 47.7122 143.875 49.0122C149.465 45.6022 152.695 35.6422 152.725 35.5322C152.835 35.1922 153.165 34.9822 153.515 35.0122C153.865 35.0522 154.145 35.3222 154.185 35.6822C154.845 41.8622 157.235 45.0622 158.725 46.4822C159.135 36.4722 162.645 30.4722 162.795 30.2122C162.945 29.9522 163.255 29.8122 163.545 29.8522C163.845 29.8922 164.085 30.1122 164.165 30.4122C164.195 30.5422 167.645 43.5522 178.975 47.3022C178.865 45.1522 178.765 40.0422 179.845 35.1122C179.915 34.7922 180.185 34.5522 180.515 34.5222C180.845 34.4922 181.145 34.6822 181.275 34.9822C181.315 35.0922 185.675 45.5522 191.405 49.0222C191.525 47.7222 191.585 45.2422 190.905 41.9822C190.825 41.6222 191.035 41.2522 191.375 41.1222C191.465 41.0922 191.545 41.0722 191.635 41.0722H191.645Z" fill="url(#paint22_linear_111_45)" />
	<g style="mix-blend-mode:overlay" opacity="0.5">
		<path d="M148.035 16.7723C148.035 16.7723 147.895 16.9722 147.625 17.3422C147.355 17.7122 146.965 18.2622 146.525 18.9522C146.305 19.3022 146.085 19.6823 145.915 20.1023C145.755 20.5123 145.625 20.9723 145.695 21.3023C145.715 21.4723 145.795 21.6022 145.885 21.7322C145.845 21.6722 145.975 21.8622 145.805 21.6122H145.815L145.835 21.6422L145.875 21.6822L145.955 21.7723C145.945 21.7023 145.885 21.6422 145.835 21.6122C145.855 21.6122 145.875 21.6122 145.895 21.6122H146.015C146.405 21.6122 147.055 21.4922 147.695 21.3222C149.005 20.9722 150.445 20.3922 152.005 19.8222C152.795 19.5222 153.595 19.2223 154.425 18.9123C155.275 18.6023 156.115 18.2822 157.135 18.0422C157.395 17.9822 157.655 17.9223 157.985 17.8823L158.235 17.8523H158.555L158.715 17.8422L158.945 17.8622C159.135 17.9022 159.195 17.8722 159.515 18.0022C159.645 18.0522 159.775 18.1123 159.905 18.1923L159.995 18.2423L160.145 18.3523L160.175 18.3823L160.325 18.5022C160.555 18.7122 160.785 18.9922 160.875 19.1222C161.115 19.4622 161.255 19.7523 161.385 20.0223C161.625 20.5423 161.795 20.9722 161.925 21.1822C162.035 21.4422 162.145 21.1522 161.405 21.0122C161.535 21.0122 161.375 20.9823 161.285 20.9923C161.195 20.9923 161.075 21.0222 161.025 21.0422L161.205 20.9622C161.375 20.8822 161.535 20.8023 161.735 20.6923L162.945 20.0022C163.815 19.5122 164.625 19.0122 165.825 18.5422C165.965 18.4822 166.135 18.4222 166.345 18.3722L166.635 18.2922C166.745 18.2722 166.915 18.2522 167.055 18.2322C167.225 18.2322 167.295 18.2022 167.545 18.2222C167.795 18.2522 168.055 18.3022 168.295 18.3922L168.385 18.4222C168.305 18.3822 168.595 18.5222 168.565 18.5122L168.605 18.5322L168.715 18.5922C168.825 18.6622 168.995 18.7722 169.045 18.8122L170.205 19.6822C170.545 19.9322 170.895 20.1422 171.125 20.2622C171.225 20.3122 171.335 20.3422 171.205 20.3122C171.205 20.3122 170.935 20.3123 170.855 20.3523L171.175 20.2723C171.755 20.1323 172.665 19.6923 173.725 19.3523C174.265 19.1823 174.885 19.0422 175.555 19.0022C175.885 18.9822 176.235 18.9922 176.575 19.0322C176.685 19.0522 176.695 19.0322 176.885 19.0722L177.055 19.1122L177.515 19.2322C179.395 19.7922 180.995 20.4122 182.565 21.0022C184.145 21.5822 185.485 22.0522 186.725 22.2122C187.335 22.2822 187.885 22.2622 188.285 22.1522C188.675 22.0322 188.935 21.8823 189.095 21.5523C189.505 20.9823 189.145 20.0522 188.755 19.3622C188.365 18.6722 187.975 18.1422 187.685 17.8122C187.405 17.4822 187.235 17.3322 187.235 17.3322C187.135 17.2422 187.125 17.0822 187.215 16.9722C187.285 16.8922 187.405 16.8622 187.495 16.9022C187.495 16.9022 187.745 17.0123 188.145 17.2723C188.545 17.5423 189.115 17.9622 189.735 18.6422C190.045 18.9822 190.375 19.3823 190.665 19.9423C190.735 20.1023 190.805 20.2123 190.865 20.4423C190.935 20.6823 190.945 20.8022 190.975 20.9322V21.2723C190.985 21.3623 190.995 21.4523 190.975 21.5523C190.965 21.7423 190.935 21.9422 190.885 22.1422C190.725 22.9622 190.025 23.8022 189.195 24.2122C188.365 24.6222 187.495 24.7522 186.655 24.7822C184.965 24.8622 183.235 24.4522 181.625 24.0422C180.815 23.8322 179.975 23.6223 179.125 23.4123C178.285 23.1823 177.415 22.9422 176.605 22.7622L176.405 22.7222L176.235 22.6923C176.315 22.7023 176.205 22.6923 176.205 22.6923C176.085 22.6923 175.975 22.6922 175.845 22.7122C175.595 22.7422 175.295 22.8322 174.945 22.9622C174.225 23.2222 173.435 23.6622 172.175 24.0622L171.805 24.1623C171.485 24.2423 170.975 24.2722 170.735 24.2222C170.125 24.1522 169.785 23.9822 169.445 23.8422C168.815 23.5422 168.345 23.2322 167.895 22.9222L166.715 22.0622C166.715 22.0622 166.735 22.0822 166.745 22.0722C166.775 22.0822 166.705 22.0522 166.695 22.0422L166.655 22.0223L166.845 22.1122C166.965 22.1722 167.105 22.2022 167.235 22.2022C167.365 22.2022 167.315 22.2122 167.365 22.2022C167.385 22.2022 167.425 22.1923 167.425 22.1923L167.365 22.2122C167.365 22.2122 167.275 22.2323 167.195 22.2723C166.575 22.4923 165.705 22.9822 164.875 23.4322L163.545 24.1422C163.315 24.2622 163.045 24.3822 162.775 24.5022L162.285 24.6923C162.125 24.7423 161.885 24.8022 161.675 24.8322C161.565 24.8422 161.465 24.8622 161.355 24.8622C161.215 24.8622 161.245 24.8622 161.205 24.8622H161.115H161.075C160.285 24.7422 160.825 24.8222 160.635 24.7822L160.575 24.7622C160.415 24.7122 160.265 24.6522 160.115 24.5822C159.835 24.4323 159.565 24.2423 159.375 24.0523C158.975 23.6623 158.755 23.2822 158.595 22.9722C158.285 22.3422 158.155 21.8722 158.015 21.5322C157.955 21.3722 157.885 21.2323 157.865 21.1923C157.825 21.1223 157.895 21.2423 157.975 21.2723C157.955 21.2523 157.895 21.2023 157.855 21.1623L157.825 21.1323C157.875 21.1723 157.685 21.0222 157.945 21.2222L157.995 21.2622C158.065 21.3122 158.145 21.3523 158.225 21.3823C158.445 21.4423 158.385 21.4323 158.455 21.4423C158.475 21.4423 158.505 21.4423 158.515 21.4423H158.505H158.475H158.375C158.245 21.4523 158.065 21.4822 157.875 21.5122C156.305 21.8222 154.545 22.3223 152.935 22.7423C151.305 23.1823 149.725 23.5323 148.165 23.7423C147.375 23.8223 146.615 23.9222 145.685 23.7322C145.565 23.7022 145.445 23.6723 145.325 23.6323C145.185 23.5723 145.055 23.5122 144.925 23.4522C144.735 23.3422 144.545 23.1823 144.405 23.0223L144.185 22.6822C144.005 22.2522 143.895 21.7823 143.935 21.3523C143.975 20.4823 144.345 19.8923 144.655 19.4123C144.985 18.9323 145.325 18.5623 145.635 18.2423C146.255 17.6023 146.795 17.1922 147.145 16.8922C147.505 16.6022 147.695 16.4522 147.695 16.4522C147.805 16.3622 147.965 16.3823 148.045 16.4923C148.115 16.5823 148.115 16.7022 148.045 16.7922L148.035 16.7723Z" fill="white" />
	</g>
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M135.995 27.0322C135.295 29.1922 134.635 31.5622 134.025 34.1822C132.415 41.1422 128.655 45.7322 127.575 46.9422C127.425 47.1122 127.485 47.3722 127.695 47.4722C130.705 48.8422 135.115 48.0022 135.115 48.0022C135.115 52.0422 136.875 55.0822 137.725 56.3022C137.895 56.5422 138.265 56.4622 138.325 56.1722C140.045 48.3822 143.645 41.8122 143.645 41.8122C142.815 45.7922 143.055 48.6522 143.205 49.7122C143.235 49.9422 143.485 50.0722 143.685 49.9722C149.955 46.7122 153.445 35.7522 153.445 35.7522C154.245 43.2822 157.605 46.6022 158.915 47.6222C159.135 47.7922 159.445 47.6322 159.455 47.3622C159.545 43.0722 160.235 39.4922 161.015 36.7422C152.235 35.6122 143.825 32.2522 135.995 27.0222V27.0322Z" fill="#203F3F" />
	</g>
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M201.255 34.1822C200.645 31.5622 199.995 29.1922 199.285 27.0322C193.385 30.9822 187.155 33.8622 180.685 35.5222C181.425 37.2222 185.835 46.9922 191.595 49.9822C191.795 50.0922 192.045 49.9522 192.075 49.7222C192.225 48.6622 192.465 45.8022 191.635 41.8222C191.635 41.8222 195.235 48.3922 196.955 56.1822C197.015 56.4722 197.385 56.5522 197.555 56.3122C198.405 55.0822 200.165 52.0522 200.165 48.0122C200.165 48.0122 204.575 48.8522 207.585 47.4822C207.795 47.3822 207.855 47.1222 207.705 46.9522C206.625 45.7422 202.865 41.1522 201.255 34.1922V34.1822Z" fill="#203F3F" />
	</g>
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M180.525 35.5623C176.325 36.6223 172.025 37.1823 167.645 37.1823C167.175 37.1823 166.715 37.1623 166.245 37.1523C168.615 41.2923 172.695 46.2323 179.325 48.1923C179.545 48.2623 179.775 48.0823 179.755 47.8423C179.645 46.2323 179.415 40.8323 180.515 35.5623H180.525Z" fill="#203F3F" />
	</g>
	<path d="M138.525 319.382C143.975 316.762 147.205 313.292 147.795 312.622L152.335 304.122V297.602C152.335 297.232 152.035 296.922 151.655 296.922H147.175C146.765 296.922 146.445 297.282 146.505 297.692C146.915 300.842 147.225 303.212 147.335 304.122L147.355 304.242L142.805 312.622C142.215 313.292 138.985 316.762 133.535 319.382H138.535H138.525Z" fill="#D89A00" />
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M138.525 319.382C143.975 316.762 147.205 313.292 147.795 312.622L152.335 304.122V297.602C152.335 297.332 152.175 297.102 151.945 296.992C150.745 297.262 149.855 298.322 149.855 299.602V303.772L145.425 311.862C141.295 315.802 137.845 317.232 137.845 317.232H137.315C136.205 317.962 134.945 318.702 133.525 319.392H138.525V319.382Z" fill="#D89A00" />
	</g>
	<path d="M151.055 299.742V304.122L146.395 312.622C142.775 316.072 139.645 317.692 138.715 318.132C138.535 318.222 138.335 318.262 138.135 318.262H135.255C135.015 318.262 134.775 318.322 134.565 318.442C134.185 318.652 133.785 318.852 133.375 319.052C125.965 322.622 126.445 330.432 126.465 330.762L126.545 331.922H162.185L162.405 330.952C164.015 323.902 163.635 318.632 163.585 317.972C163.585 311.432 163.205 305.262 163.155 304.432C163.335 302.132 163.515 299.882 163.675 297.662C163.705 297.272 163.395 296.942 163.005 296.942H153.865C152.315 296.942 151.055 298.202 151.055 299.752V299.742Z" fill="#D89A00" />
	<path style="mix-blend-mode:multiply" opacity="0.5" d="M127.245 331.162H161.585L161.675 330.772C163.265 323.802 162.885 318.592 162.835 318.022V317.962C162.835 311.572 162.475 305.602 162.405 304.472V304.422V304.372C162.585 302.102 162.755 299.882 162.925 297.692H153.865C152.725 297.692 151.805 298.622 151.805 299.752V304.332L147.005 313.102L146.925 313.182C143.205 316.732 139.955 318.402 139.045 318.832C138.765 318.962 138.455 319.032 138.145 319.032H135.265C135.145 319.032 135.035 319.062 134.925 319.122C134.535 319.332 134.125 319.542 133.705 319.742C126.745 323.092 127.195 330.412 127.225 330.722L127.255 331.182L127.245 331.162Z" fill="url(#paint23_linear_111_45)" />
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M160.455 304.012C160.455 304.012 162.145 309.262 162.145 312.702C162.145 316.142 160.015 325.742 154.205 330.442C154.205 330.442 153.725 331.082 152.615 331.912H162.175L162.395 330.942C164.005 323.892 163.625 318.622 163.575 317.962C163.575 311.422 163.195 305.252 163.145 304.422C163.325 302.122 163.505 299.872 163.665 297.652C163.665 297.652 162.625 302.702 160.445 304.012H160.455Z" fill="#D89A00" />
	</g>
	<g style="mix-blend-mode:multiply" opacity="0.25">
		<path d="M152.335 331.912H162.185L162.405 330.942C164.015 323.892 163.635 318.622 163.585 317.962C163.585 317.962 155.025 321.012 152.335 331.912Z" fill="#D89A00" />
	</g>
	<path d="M163.895 334.212H124.835C124.665 334.212 124.515 334.072 124.515 333.892V332.092C124.515 331.302 125.155 330.662 125.945 330.662H152.335L162.605 329.432C163.455 329.332 164.205 329.992 164.205 330.852V333.892C164.205 334.062 164.065 334.212 163.885 334.212H163.895Z" fill="#223A39" />
	<path style="mix-blend-mode:multiply" opacity="0.7" d="M125.275 333.462H163.455V330.862C163.455 330.662 163.375 330.482 163.225 330.352C163.075 330.222 162.885 330.162 162.695 330.182L152.335 331.412H125.945C125.575 331.412 125.265 331.712 125.265 332.092V333.462H125.275Z" fill="url(#paint24_linear_111_45)" />
	<path d="M147.335 304.132H152.335" stroke="#AA6400" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
	<path d="M145.955 306.682H150.975" stroke="#AA6400" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
	<path d="M144.645 309.232H149.645" stroke="#AA6400" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
	<path d="M143.255 311.782H148.225" stroke="#AA6400" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
	<path d="M141.075 314.332H146.075" stroke="#AA6400" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
	<path d="M137.835 316.882H142.735" stroke="#AA6400" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M163.895 334.212C164.065 334.212 164.215 334.072 164.215 333.892V330.852C164.215 329.992 163.465 329.332 162.615 329.432L154.215 330.432C154.215 330.432 152.555 332.642 148.295 334.202H163.905L163.895 334.212Z" fill="#223A39" />
	</g>
	<path d="M206.905 202.412C206.905 202.412 201.085 207.402 198.855 208.432C196.415 209.562 190.215 209.992 189.945 208.462C189.735 207.232 193.135 206.412 196.355 205.762L200.375 202.352L206.905 202.412Z" fill="#C39173" />
	<path d="M206.905 202.412C206.905 202.412 202.385 209.772 200.895 211.732C199.405 213.692 194.895 218.762 193.545 217.412C192.445 216.312 195.515 212.072 197.255 209.532L200.375 202.352L206.905 202.412Z" fill="#C39173" />
	<path d="M206.905 202.412C206.905 202.412 202.395 209.512 200.205 210.622C198.015 211.732 191.475 214.252 190.845 212.442C190.335 210.972 194.955 208.502 197.625 206.982L200.385 202.362L206.915 202.422L206.905 202.412Z" fill="#C39173" />
	<g style="mix-blend-mode:multiply">
		<path d="M189.945 208.462C189.735 207.232 193.135 206.412 196.355 205.762L200.375 202.352L206.905 202.412C206.905 202.412 202.385 209.772 200.895 211.732C199.405 213.692 194.895 218.762 193.545 217.412C192.825 216.692 193.905 214.602 195.225 212.542C193.125 213.142 191.175 213.382 190.845 212.442C190.565 211.642 191.815 210.542 193.445 209.462C191.625 209.502 190.085 209.222 189.955 208.472L189.945 208.462Z" fill="#C39173" />
	</g>
	<path d="M189.075 94.2323L189.175 94.2623C194.335 95.9323 198.095 100.402 198.845 105.782C200.265 115.932 202.605 132.722 204.135 144.332L205.935 153.882C206.695 157.052 207.015 160.312 206.885 163.572L206.095 186.082C206.095 186.082 207.175 196.772 206.915 202.402C206.615 208.732 205.445 210.272 204.565 212.202C203.425 214.712 200.255 219.742 199.105 218.902C197.945 218.052 199.185 213.512 200.915 210.302C200.915 210.302 200.805 205.892 200.395 202.342C199.985 198.792 198.305 195.982 198.305 195.982C198.305 195.982 198.405 198.972 197.955 201.392C197.365 204.562 196.515 206.262 195.375 206.262C194.235 206.262 193.745 201.632 193.575 198.062C193.415 194.492 194.905 186.082 194.905 186.082C194.905 186.082 192.635 168.142 191.955 162.152C191.445 157.702 190.095 144.322 190.095 144.322L187.315 124.652L189.095 94.2223L189.075 94.2323Z" fill="#C39173" />
	<path style="mix-blend-mode:multiply" opacity="0.5" d="M189.765 95.2822C194.195 97.0522 197.435 101.132 198.095 105.892C199.695 117.292 201.905 133.232 203.385 144.432L205.195 154.032C205.945 157.172 206.265 160.362 206.135 163.552L205.345 186.072C205.345 186.072 205.345 186.142 205.345 186.172C205.355 186.282 206.415 196.862 206.155 202.382C205.905 207.722 205.015 209.532 204.235 211.132C204.105 211.392 203.985 211.652 203.865 211.912C202.675 214.522 200.345 217.862 199.475 218.232C199.125 217.542 199.705 214.112 201.555 210.672C201.615 210.562 201.645 210.432 201.645 210.302C201.645 210.262 201.535 205.812 201.125 202.272C200.695 198.602 199.005 195.732 198.935 195.612C198.755 195.322 198.405 195.182 198.085 195.282C197.755 195.382 197.535 195.682 197.545 196.022C197.545 196.052 197.635 198.962 197.205 201.272C196.545 204.802 195.765 205.412 195.465 205.512C195.135 205.082 194.545 203.092 194.315 198.052C194.155 194.602 195.625 186.322 195.635 186.232C195.645 186.162 195.655 186.082 195.635 186.002C195.615 185.822 193.355 168.002 192.685 162.082C192.185 157.682 190.835 144.392 190.825 144.262L188.055 124.642L189.765 95.2822Z" fill="url(#paint25_linear_111_45)" />
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M189.075 94.2323L189.175 94.2623C194.335 95.9323 198.085 100.402 198.845 105.772C199.985 113.882 201.705 126.242 203.135 136.812C200.975 137.692 197.955 138.842 195.025 139.632L199.795 174.432C199.825 174.622 199.705 174.792 199.525 174.842C198.835 175.022 197.155 175.462 195.845 175.762C195.845 175.762 196.065 192.022 195.525 206.252C195.475 206.252 195.415 206.272 195.365 206.272C194.215 206.272 193.735 201.642 193.565 198.072C193.405 194.502 194.895 186.092 194.895 186.092C194.895 186.092 192.625 168.152 191.945 162.162C191.435 157.712 190.085 144.332 190.085 144.332L187.305 124.662L189.085 94.2323H189.075Z" fill="#C39173" />
	</g>
	<path d="M189.405 93.5523C194.805 95.3023 198.795 100.062 199.585 105.672C200.765 114.122 204.775 124.182 206.145 133.812C206.175 134.022 206.055 134.232 205.855 134.302C199.725 136.572 192.765 138.362 188.895 138.482C188.665 138.482 188.475 138.322 188.435 138.092L186.555 124.762V124.692L188.385 93.2223L189.405 93.5523Z" fill="#EFB20C" />
	<path style="mix-blend-mode:multiply" opacity="0.5" d="M201.955 119.102C200.655 114.392 199.415 109.932 198.835 105.782C198.085 100.452 194.295 95.9323 189.165 94.2623L189.065 94.2323L187.285 124.662L189.125 137.722C192.775 137.542 199.225 135.942 205.355 133.682C204.645 128.852 203.275 123.902 201.945 119.102H201.955Z" fill="url(#paint26_linear_111_45)" />
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M192.395 115.572C192.395 115.572 195.145 125.352 196.705 133.682C196.705 133.682 200.995 133.872 206.015 132.982C206.055 133.262 206.105 133.542 206.145 133.822C206.175 134.032 206.055 134.242 205.855 134.312C199.725 136.582 192.765 138.372 188.895 138.492C188.665 138.492 188.475 138.332 188.445 138.102L186.565 124.772V124.702L188.395 93.2323L192.405 115.582L192.395 115.572Z" fill="#EFB20C" />
	</g>
	<path d="M193.175 169.572L190.875 149.382H144.425L142.125 169.562C140.205 179.482 139.585 194.902 140.285 215.412C140.785 229.972 140.915 259.402 142.405 269.802C143.155 275.082 144.305 283.682 145.265 291.002H164.165C165.255 274.662 166.595 200.012 166.815 187.332H168.505C168.725 200.012 170.055 274.672 171.155 291.002H190.055C191.015 283.682 192.155 275.082 192.915 269.802C194.405 259.402 194.535 229.972 195.035 215.412C195.735 194.902 195.115 179.482 193.195 169.562L193.175 169.572Z" fill="#316569" />
	<path style="mix-blend-mode:multiply" opacity="0.7" d="M171.835 290.262H189.365C190.595 280.892 191.525 273.982 192.135 269.702C193.205 262.232 193.575 244.492 193.885 230.242C194.005 224.682 194.115 219.442 194.255 215.392C194.955 194.942 194.335 179.572 192.425 169.712C192.425 169.692 192.425 169.672 192.425 169.652L190.195 150.132H145.095L142.865 169.652C142.865 169.652 142.865 169.692 142.865 169.712C140.955 179.572 140.345 194.942 141.035 215.392C141.175 219.442 141.285 224.692 141.405 230.242C141.705 244.492 142.085 262.232 143.155 269.702C143.915 275.032 145.065 283.692 145.925 290.262H163.455C164.525 272.782 165.805 201.592 166.055 187.322C166.055 186.912 166.395 186.582 166.805 186.582H168.495C168.905 186.582 169.235 186.912 169.245 187.322C169.495 201.592 170.775 272.772 171.845 290.262H171.835Z" fill="url(#paint27_linear_111_45)" />
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M144.425 149.382L142.125 169.562C141.595 172.322 141.155 175.512 140.825 179.122C146.265 180.402 157.405 182.672 167.655 182.672C177.905 182.672 189.045 180.402 194.485 179.122C194.155 175.512 193.715 172.322 193.185 169.562L190.885 149.372H144.425V149.382Z" fill="#316569" />
	</g>
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M168.495 187.352C168.715 200.072 170.045 274.682 171.145 291.012H190.045C190.225 289.642 190.405 288.232 190.595 286.812L175.445 284.682C173.275 258.852 173.275 237.852 173.275 237.852C169.945 225.852 168.495 187.342 168.495 187.342V187.352Z" fill="#316569" />
	</g>
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M159.855 284.682L144.705 286.812C144.895 288.242 145.075 289.652 145.255 291.012H164.155C165.245 274.672 166.585 200.022 166.805 187.342C166.805 187.342 165.355 225.852 162.025 237.852C162.025 237.852 162.025 258.852 159.855 284.682Z" fill="#316569" />
	</g>
	<path d="M163.955 294.562H145.395C144.675 294.562 144.075 294.032 143.975 293.322L143.415 289.102C143.305 288.242 143.965 287.482 144.835 287.482H164.315C165.155 287.482 165.815 288.202 165.745 289.032L165.385 293.252C165.325 293.992 164.705 294.562 163.955 294.562Z" fill="#599091" />
	<path d="M171.335 294.562H189.895C190.615 294.562 191.215 294.032 191.315 293.322L191.875 289.102C191.985 288.242 191.325 287.482 190.455 287.482H170.975C170.135 287.482 169.475 288.202 169.545 289.032L169.905 293.252C169.965 293.992 170.585 294.562 171.335 294.562Z" fill="#599091" />
	<path style="mix-blend-mode:multiply" opacity="0.7" d="M144.835 288.222C144.635 288.222 144.455 288.302 144.325 288.452C144.195 288.602 144.135 288.792 144.165 288.992L144.725 293.212C144.765 293.552 145.065 293.802 145.405 293.802H163.965C164.315 293.802 164.615 293.532 164.645 293.182L165.005 288.962C165.025 288.772 164.955 288.582 164.825 288.442C164.695 288.302 164.515 288.222 164.325 288.222H144.845H144.835Z" fill="url(#paint28_linear_111_45)" />
	<path style="mix-blend-mode:multiply" opacity="0.7" d="M170.975 288.222C170.785 288.222 170.605 288.302 170.475 288.442C170.345 288.582 170.285 288.772 170.295 288.962L170.655 293.182C170.685 293.532 170.985 293.802 171.335 293.802H189.895C190.235 293.802 190.525 293.552 190.575 293.212L191.135 288.992C191.165 288.792 191.105 288.602 190.975 288.452C190.845 288.302 190.665 288.222 190.465 288.222H170.985H170.975Z" fill="url(#paint29_linear_111_45)" />
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M141.865 177.062C141.865 177.062 152.445 170.352 152.445 158.352" stroke="#316569" stroke-linecap="round" stroke-linejoin="round" />
	</g>
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M193.425 177.062C193.425 177.062 182.845 170.352 182.845 158.352" stroke="#316569" stroke-linecap="round" stroke-linejoin="round" />
	</g>
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M167.645 150.132V186.592" stroke="#316569" stroke-linecap="round" stroke-linejoin="round" />
	</g>
	<path d="M196.755 319.382C191.305 316.762 188.075 313.292 187.485 312.622L182.945 304.122V297.602C182.945 297.232 183.245 296.922 183.625 296.922H188.105C188.515 296.922 188.835 297.282 188.775 297.692C188.365 300.842 188.055 303.212 187.945 304.122L187.925 304.242L192.475 312.622C193.065 313.292 196.295 316.762 201.745 319.382H196.745H196.755Z" fill="#D89A00" />
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M196.755 319.382C191.305 316.762 188.075 313.292 187.485 312.622L182.945 304.122V297.602C182.945 297.332 183.105 297.102 183.335 296.992C184.535 297.262 185.425 298.322 185.425 299.602V303.772L189.855 311.862C193.985 315.802 197.435 317.232 197.435 317.232H197.965C199.075 317.962 200.335 318.702 201.755 319.392H196.755V319.382Z" fill="#D89A00" />
	</g>
	<path d="M184.235 299.742V304.122L188.895 312.622C192.515 316.072 195.645 317.692 196.575 318.132C196.755 318.222 196.955 318.262 197.155 318.262H200.035C200.275 318.262 200.515 318.322 200.725 318.442C201.105 318.652 201.505 318.852 201.915 319.052C209.325 322.622 208.845 330.432 208.825 330.762L208.745 331.922H173.105L172.885 330.952C171.275 323.902 171.655 318.632 171.705 317.972C171.705 311.432 172.085 305.262 172.135 304.432C171.955 302.132 171.775 299.882 171.615 297.662C171.585 297.272 171.895 296.942 172.285 296.942H181.425C182.975 296.942 184.235 298.202 184.235 299.752V299.742Z" fill="#D89A00" />
	<path style="mix-blend-mode:multiply" opacity="0.5" d="M208.075 330.702C208.095 330.392 208.555 323.082 201.595 319.722C201.175 319.522 200.765 319.312 200.375 319.102C200.265 319.042 200.155 319.012 200.045 319.012H197.165C196.845 319.012 196.545 318.942 196.265 318.812C195.355 318.382 192.105 316.712 188.385 313.162L188.305 313.082L183.505 304.312V299.732C183.505 298.592 182.575 297.672 181.445 297.672H172.385C172.545 299.862 172.725 302.092 172.905 304.352V304.402V304.452C172.835 305.582 172.475 311.552 172.475 317.942V318.002C172.425 318.572 172.045 323.782 173.635 330.752L173.725 331.142H208.065L208.095 330.682L208.075 330.702Z" fill="url(#paint30_linear_111_45)" />
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M174.835 304.012C174.835 304.012 173.145 309.262 173.145 312.702C173.145 316.142 175.275 325.742 181.085 330.442C181.085 330.442 181.565 331.082 182.675 331.912H173.115L172.895 330.942C171.285 323.892 171.665 318.622 171.715 317.962C171.715 311.422 172.095 305.252 172.145 304.422C171.965 302.122 171.785 299.872 171.625 297.652C171.625 297.652 172.665 302.702 174.845 304.012H174.835Z" fill="#D89A00" />
	</g>
	<g style="mix-blend-mode:multiply" opacity="0.25">
		<path d="M182.955 331.912H173.105L172.885 330.942C171.275 323.892 171.655 318.622 171.705 317.962C171.705 317.962 180.265 321.012 182.955 331.912Z" fill="#D89A00" />
	</g>
	<path d="M171.395 334.212H210.445C210.615 334.212 210.765 334.072 210.765 333.892V332.092C210.765 331.302 210.125 330.662 209.335 330.662H182.945L172.675 329.432C171.825 329.332 171.075 329.992 171.075 330.852V333.892C171.075 334.062 171.215 334.212 171.395 334.212Z" fill="#223A39" />
	<path style="mix-blend-mode:multiply" opacity="0.7" d="M210.015 332.092C210.015 331.722 209.715 331.412 209.335 331.412H182.945L172.585 330.182C172.395 330.162 172.205 330.222 172.055 330.352C171.905 330.482 171.825 330.662 171.825 330.862V333.462H210.005V332.092H210.015Z" fill="url(#paint31_linear_111_45)" />
	<path d="M187.955 304.132H182.955" stroke="#AA6400" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
	<path d="M189.335 306.682H184.315" stroke="#AA6400" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
	<path d="M190.645 309.232H185.645" stroke="#AA6400" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
	<path d="M192.035 311.782H187.065" stroke="#AA6400" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
	<path d="M194.205 314.332H189.205" stroke="#AA6400" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
	<path d="M197.455 316.882H192.545" stroke="#AA6400" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M171.395 334.212C171.225 334.212 171.075 334.072 171.075 333.892V330.852C171.075 329.992 171.825 329.332 172.675 329.432L181.075 330.432C181.075 330.432 182.735 332.642 186.995 334.202H171.385L171.395 334.212Z" fill="#223A39" />
	</g>
	<path d="M195.905 173.742C196.115 173.682 196.255 173.482 196.235 173.272L193.915 149.422L189.825 93.6723L175.555 89.5823C175.435 89.5523 175.315 89.5723 175.215 89.6323C173.025 91.0223 170.435 91.8223 167.645 91.8223C164.855 91.8223 162.265 91.0223 160.075 89.6323C159.975 89.5723 159.855 89.5523 159.735 89.5823L145.465 93.6723L141.375 149.422L139.055 173.272C139.035 173.492 139.175 173.692 139.385 173.742C141.765 174.372 155.385 177.802 167.645 177.802C179.905 177.802 193.525 174.362 195.905 173.742Z" fill="#EFB20C" />
	<path style="mix-blend-mode:multiply" opacity="0.5" d="M139.825 173.082C142.775 173.842 155.915 177.062 167.645 177.062C179.375 177.062 192.515 173.852 195.465 173.082L193.165 149.492L189.105 94.2423L175.485 90.3323C173.125 91.7923 170.425 92.5623 167.645 92.5623C164.865 92.5623 162.165 91.7923 159.805 90.3323L146.185 94.2423L142.135 149.472L139.835 173.082H139.825Z" fill="url(#paint32_linear_111_45)" />
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M140.765 170.552C145.125 171.632 156.905 174.262 167.645 174.262C178.385 174.262 190.175 171.622 194.525 170.552" stroke="#EFB20C" stroke-width="0.5" stroke-linecap="round" stroke-linejoin="round" />
	</g>
	<g style="mix-blend-mode:multiply" opacity="0.5">
		<path d="M177.215 90.8323C174.525 92.7823 171.215 93.9423 167.645 93.9423C164.075 93.9423 160.755 92.7923 158.075 90.8323" stroke="#EFB20C" stroke-width="0.5" stroke-linecap="round" stroke-linejoin="round" />
	</g>
	<path d="M169 0L168.058 339.999" stroke="#3D85EB" stroke-width="3" stroke-dasharray="6 6" />
	<path d="M48 0L47.0582 339.999" stroke="#3D85EB" stroke-width="3" stroke-dasharray="6 6" />
	<defs>
		<linearGradient id="paint0_linear_111_45" x1="50.3811" y1="185.464" x2="50.3811" y2="329.964" gradientUnits="userSpaceOnUse">
			<stop stop-color="#C39173" />
			<stop offset="1" stop-color="#C39173" stop-opacity="0" />
		</linearGradient>
		<linearGradient id="paint1_linear_111_45" x1="51.281" y1="331.214" x2="51.281" y2="297.734" gradientUnits="userSpaceOnUse">
			<stop stop-color="#D89A00" />
			<stop offset="1" stop-color="#D89A00" stop-opacity="0" />
		</linearGradient>
		<linearGradient id="paint2_linear_111_45" x1="28.5411" y1="331.874" x2="75.3011" y2="331.874" gradientUnits="userSpaceOnUse">
			<stop stop-color="#223A39" />
			<stop offset="1" stop-color="#223A39" stop-opacity="0" />
		</linearGradient>
		<linearGradient id="paint3_linear_111_45" x1="44.601" y1="184.214" x2="44.601" y2="290.314" gradientUnits="userSpaceOnUse">
			<stop stop-color="#316569" />
			<stop offset="1" stop-color="#316569" stop-opacity="0" />
		</linearGradient>
		<linearGradient id="paint4_linear_111_45" x1="36.9011" y1="293.864" x2="36.9011" y2="288.274" gradientUnits="userSpaceOnUse">
			<stop stop-color="#599091" />
			<stop offset="1" stop-color="#599091" stop-opacity="0" />
		</linearGradient>
		<linearGradient id="paint5_linear_111_45" x1="55.4711" y1="76.694" x2="55.4711" y2="329.964" gradientUnits="userSpaceOnUse">
			<stop stop-color="#C39173" stop-opacity="0.05" />
			<stop offset="0.3" stop-color="#C39173" />
			<stop offset="1" stop-color="#C39173" stop-opacity="0" />
		</linearGradient>
		<linearGradient id="paint6_linear_111_45" x1="47.2511" y1="11.9639" x2="47.2511" y2="82.8739" gradientUnits="userSpaceOnUse">
			<stop stop-color="#C39173" />
			<stop offset="1" stop-color="#C39173" stop-opacity="0" />
		</linearGradient>
		<linearGradient id="paint7_linear_111_45" x1="42.4111" y1="81.494" x2="42.4111" y2="6.47398" gradientUnits="userSpaceOnUse">
			<stop stop-color="#203F3F" />
			<stop offset="1" stop-color="#203F3F" stop-opacity="0" />
		</linearGradient>
		<linearGradient id="paint8_linear_111_45" x1="43.5211" y1="11.904" x2="43.5211" y2="82.804" gradientUnits="userSpaceOnUse">
			<stop stop-color="#C39173" />
			<stop offset="1" stop-color="#C39173" stop-opacity="0" />
		</linearGradient>
		<linearGradient id="paint9_linear_111_45" x1="47.5011" y1="150.194" x2="47.5011" y2="290.314" gradientUnits="userSpaceOnUse">
			<stop stop-color="#316569" />
			<stop offset="1" stop-color="#316569" stop-opacity="0" />
		</linearGradient>
		<linearGradient id="paint10_linear_111_45" x1="44.8611" y1="293.864" x2="44.8611" y2="288.274" gradientUnits="userSpaceOnUse">
			<stop stop-color="#599091" />
			<stop offset="1" stop-color="#599091" stop-opacity="0" />
		</linearGradient>
		<linearGradient id="paint11_linear_111_45" x1="59.4911" y1="331.214" x2="59.4911" y2="297.734" gradientUnits="userSpaceOnUse">
			<stop stop-color="#D89A00" />
			<stop offset="1" stop-color="#D89A00" stop-opacity="0" />
		</linearGradient>
		<linearGradient id="paint12_linear_111_45" x1="36.7411" y1="331.874" x2="83.5011" y2="331.874" gradientUnits="userSpaceOnUse">
			<stop stop-color="#223A39" />
			<stop offset="1" stop-color="#223A39" stop-opacity="0" />
		</linearGradient>
		<linearGradient id="paint13_linear_111_45" x1="47.021" y1="176.364" x2="47.021" y2="90.834" gradientUnits="userSpaceOnUse">
			<stop stop-color="#EFB20C" />
			<stop offset="1" stop-color="#EFB20C" stop-opacity="0" />
		</linearGradient>
		<linearGradient id="paint14_linear_111_45" x1="36.9411" y1="94.894" x2="36.9411" y2="218.314" gradientUnits="userSpaceOnUse">
			<stop stop-color="#C39173" />
			<stop offset="1" stop-color="#C39173" stop-opacity="0" />
		</linearGradient>
		<linearGradient id="paint15_linear_111_45" x1="40.1411" y1="176.904" x2="40.1411" y2="89.234" gradientUnits="userSpaceOnUse">
			<stop stop-color="#EFB20C" />
			<stop offset="1" stop-color="#EFB20C" stop-opacity="0" />
		</linearGradient>
		<linearGradient id="paint16_linear_111_45" x1="138.165" y1="95.2822" x2="138.165" y2="218.232" gradientUnits="userSpaceOnUse">
			<stop stop-color="#C39173" />
			<stop offset="1" stop-color="#C39173" stop-opacity="0" />
		</linearGradient>
		<linearGradient id="paint17_linear_111_45" x1="138.955" y1="176.852" x2="138.955" y2="89.1823" gradientUnits="userSpaceOnUse">
			<stop stop-color="#EFB20C" />
			<stop offset="1" stop-color="#EFB20C" stop-opacity="0" />
		</linearGradient>
		<linearGradient id="paint18_linear_111_45" x1="128.455" y1="206.052" x2="206.835" y2="206.052" gradientUnits="userSpaceOnUse">
			<stop stop-color="#C39173" />
			<stop offset="1" stop-color="#C39173" stop-opacity="0" />
		</linearGradient>
		<linearGradient id="paint19_linear_111_45" x1="199.105" y1="51.6622" x2="199.105" y2="62.7222" gradientUnits="userSpaceOnUse">
			<stop stop-color="#C39173" />
			<stop offset="1" stop-color="#C39173" stop-opacity="0" />
		</linearGradient>
		<linearGradient id="paint20_linear_111_45" x1="136.185" y1="51.6622" x2="136.185" y2="62.7222" gradientUnits="userSpaceOnUse">
			<stop stop-color="#C39173" />
			<stop offset="1" stop-color="#C39173" stop-opacity="0" />
		</linearGradient>
		<linearGradient id="paint21_linear_111_45" x1="167.645" y1="11.8823" x2="167.645" y2="84.1423" gradientUnits="userSpaceOnUse">
			<stop stop-color="#C39173" />
			<stop offset="1" stop-color="#C39173" stop-opacity="0" />
		</linearGradient>
		<linearGradient id="paint22_linear_111_45" x1="167.645" y1="55.0622" x2="167.645" y2="6.49224" gradientUnits="userSpaceOnUse">
			<stop stop-color="#203F3F" />
			<stop offset="1" stop-color="#203F3F" stop-opacity="0" />
		</linearGradient>
		<linearGradient id="paint23_linear_111_45" x1="145.065" y1="331.162" x2="145.065" y2="297.682" gradientUnits="userSpaceOnUse">
			<stop stop-color="#D89A00" />
			<stop offset="1" stop-color="#D89A00" stop-opacity="0" />
		</linearGradient>
		<linearGradient id="paint24_linear_111_45" x1="163.455" y1="331.822" x2="125.275" y2="331.822" gradientUnits="userSpaceOnUse">
			<stop stop-color="#223A39" />
			<stop offset="1" stop-color="#223A39" stop-opacity="0" />
		</linearGradient>
		<linearGradient id="paint25_linear_111_45" x1="197.125" y1="95.2822" x2="197.125" y2="218.232" gradientUnits="userSpaceOnUse">
			<stop stop-color="#C39173" />
			<stop offset="1" stop-color="#C39173" stop-opacity="0" />
		</linearGradient>
		<linearGradient id="paint26_linear_111_45" x1="196.335" y1="176.852" x2="196.335" y2="89.1823" gradientUnits="userSpaceOnUse">
			<stop stop-color="#EFB20C" />
			<stop offset="1" stop-color="#EFB20C" stop-opacity="0" />
		</linearGradient>
		<linearGradient id="paint27_linear_111_45" x1="167.645" y1="150.132" x2="167.645" y2="290.262" gradientUnits="userSpaceOnUse">
			<stop stop-color="#316569" />
			<stop offset="1" stop-color="#316569" stop-opacity="0" />
		</linearGradient>
		<linearGradient id="paint28_linear_111_45" x1="154.575" y1="293.812" x2="154.575" y2="288.222" gradientUnits="userSpaceOnUse">
			<stop stop-color="#599091" />
			<stop offset="1" stop-color="#599091" stop-opacity="0" />
		</linearGradient>
		<linearGradient id="paint29_linear_111_45" x1="180.715" y1="293.812" x2="180.715" y2="288.222" gradientUnits="userSpaceOnUse">
			<stop stop-color="#599091" />
			<stop offset="1" stop-color="#599091" stop-opacity="0" />
		</linearGradient>
		<linearGradient id="paint30_linear_111_45" x1="190.225" y1="331.162" x2="190.225" y2="297.682" gradientUnits="userSpaceOnUse">
			<stop stop-color="#D89A00" />
			<stop offset="1" stop-color="#D89A00" stop-opacity="0" />
		</linearGradient>
		<linearGradient id="paint31_linear_111_45" x1="171.835" y1="331.822" x2="210.015" y2="331.822" gradientUnits="userSpaceOnUse">
			<stop stop-color="#223A39" />
			<stop offset="1" stop-color="#223A39" stop-opacity="0" />
		</linearGradient>
		<linearGradient id="paint32_linear_111_45" x1="167.645" y1="176.852" x2="167.645" y2="89.1823" gradientUnits="userSpaceOnUse">
			<stop stop-color="#EFB20C" />
			<stop offset="1" stop-color="#EFB20C" stop-opacity="0" />
		</linearGradient>
	</defs>
</svg>

```

## Components/Shared/Icon/IconSettings.razor
```razor
﻿<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
	<g fill="none" stroke="currentColor" stroke-width="1.5">
		<circle cx="12" cy="12" r="3" />
		<path d="M13.765 2.152C13.398 2 12.932 2 12 2s-1.398 0-1.765.152a2 2 0 0 0-1.083 1.083c-.092.223-.129.484-.143.863a1.62 1.62 0 0 1-.79 1.353a1.62 1.62 0 0 1-1.567.008c-.336-.178-.579-.276-.82-.308a2 2 0 0 0-1.478.396C4.04 5.79 3.806 6.193 3.34 7s-.7 1.21-.751 1.605a2 2 0 0 0 .396 1.479c.148.192.355.353.676.555c.473.297.777.803.777 1.361s-.304 1.064-.777 1.36c-.321.203-.529.364-.676.556a2 2 0 0 0-.396 1.479c.052.394.285.798.75 1.605c.467.807.7 1.21 1.015 1.453a2 2 0 0 0 1.479.396c.24-.032.483-.13.819-.308a1.62 1.62 0 0 1 1.567.008c.483.28.77.795.79 1.353c.014.38.05.64.143.863a2 2 0 0 0 1.083 1.083C10.602 22 11.068 22 12 22s1.398 0 1.765-.152a2 2 0 0 0 1.083-1.083c.092-.223.129-.483.143-.863c.02-.558.307-1.074.79-1.353a1.62 1.62 0 0 1 1.567-.008c.336.178.579.276.819.308a2 2 0 0 0 1.479-.396c.315-.242.548-.646 1.014-1.453s.7-1.21.751-1.605a2 2 0 0 0-.396-1.479c-.148-.192-.355-.353-.676-.555A1.62 1.62 0 0 1 19.562 12c0-.558.304-1.064.777-1.36c.321-.203.529-.364.676-.556a2 2 0 0 0 .396-1.479c-.052-.394-.285-.798-.75-1.605c-.467-.807-.7-1.21-1.015-1.453a2 2 0 0 0-1.479-.396c-.24.032-.483.13-.82.308a1.62 1.62 0 0 1-1.566-.008a1.62 1.62 0 0 1-.79-1.353c-.014-.38-.05-.64-.143-.863a2 2 0 0 0-1.083-1.083Z" />
	</g>
</svg>
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
             xmlns:components="clr-namespace:create4care.Components"
             x:Class="create4care.MainPage">

    <BlazorWebView x:Name="blazorWebView" HostPage="wwwroot/index.html">
        <BlazorWebView.RootComponents>
            <RootComponent Selector="#app" ComponentType="{x:Type components:Routes}" />
        </BlazorWebView.RootComponents>
    </BlazorWebView>

</ContentPage>

```

## MainPage.xaml.cs
```cs
﻿namespace create4care
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
﻿using Microsoft.AspNetCore.Components.WebView.Maui;
using Microsoft.Extensions.Logging;
using create4care.Components.Services;

namespace create4care
{
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

            #if ANDROID
            builder.ConfigureMauiHandlers(handlers =>
            {
                handlers.AddHandler<BlazorWebView, CustomBlazorWebViewHandler>();
            });
#endif

#if DEBUG
            builder.Services.AddBlazorWebViewDeveloperTools();
            builder.Logging.AddDebug();
            #endif

            return builder.Build();
        }
    }
}

```

## Platforms/Android/AndroidManifest.xml
```xml
﻿<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <application android:allowBackup="true" android:icon="@mipmap/appicon" android:roundIcon="@mipmap/appicon_round" android:supportsRtl="true"></application>
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <uses-permission android:name="android.permission.INTERNET" />
    
    <uses-permission android:name="android.permission.CAMERA" />

    <uses-permission android:name="android.permission.BLUETOOTH" />
	<uses-permission android:name="android.permission.BLUETOOTH_ADMIN" />
    <uses-permission android:name="android.permission.BLUETOOTH_SCAN" android:usesPermissionFlags="neverForLocation" />
	<uses-permission android:name="android.permission.BLUETOOTH_CONNECT" />
</manifest>
```

## Platforms/Android/CustomBlazorWebViewHandler.cs
```cs
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

```

## Platforms/Android/MainActivity.cs
```cs
﻿using Android;
using Android.App;
using Android.Content.PM;
using Android.OS;
using System.Runtime.Versioning;

namespace create4care;

[Activity(Theme = "@style/Maui.SplashTheme", MainLauncher = true, ConfigurationChanges = ConfigChanges.ScreenSize | ConfigChanges.Orientation | ConfigChanges.UiMode | ConfigChanges.ScreenLayout | ConfigChanges.SmallestScreenSize | ConfigChanges.Density)]
[SupportedOSPlatform("android31.0")] 
public class MainActivity : MauiAppCompatActivity
{
    protected override void OnCreate(Bundle? savedInstanceState)
    {
        base.OnCreate(savedInstanceState);

        if (Build.VERSION.SdkInt >= BuildVersionCodes.S)
        {
            if (CheckSelfPermission(Manifest.Permission.Camera) != Permission.Granted ||
                CheckSelfPermission(Manifest.Permission.BluetoothScan) != Permission.Granted ||
                CheckSelfPermission(Manifest.Permission.BluetoothConnect) != Permission.Granted
                )
            {
                RequestPermissions(
                [
                    Manifest.Permission.Camera,
                    Manifest.Permission.BluetoothScan,
                    Manifest.Permission.BluetoothConnect,
                ], 0);
            }
        }
    }
}

```

## Platforms/Android/MainApplication.cs
```cs
﻿using Android.App;
using Android.Runtime;

namespace create4care
{
    [Application]
    public class MainApplication : MauiApplication
    {
        public MainApplication(IntPtr handle, JniHandleOwnership ownership)
            : base(handle, ownership)
        {
        }

        protected override MauiApp CreateMauiApp() => MauiProgram.CreateMauiApp();
    }
}

```

## Platforms/Android/Resources/values/colors.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="colorPrimary">#3D85EB</color>
    <color name="colorPrimaryDark">#145DC2</color>
    <color name="colorAccent">#2C71A5</color>
</resources>
```

## Platforms/MacCatalyst/AppDelegate.cs
```cs
﻿using Foundation;

namespace create4care
{
    [Register("AppDelegate")]
    public class AppDelegate : MauiUIApplicationDelegate
    {
        protected override MauiApp CreateMauiApp() => MauiProgram.CreateMauiApp();
    }
}

```

## Platforms/MacCatalyst/Entitlements.plist
```plist
﻿<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
    <!-- See https://aka.ms/maui-publish-app-store#add-entitlements for more information about adding entitlements.-->
    <dict>
        <!-- App Sandbox must be enabled to distribute a MacCatalyst app through the Mac App Store. -->
        <key>com.apple.security.app-sandbox</key>
        <true/>
        <!-- When App Sandbox is enabled, this value is required to open outgoing network connections. -->
        <key>com.apple.security.network.client</key>
        <true/>
    </dict>
</plist>


```

## Platforms/MacCatalyst/Info.plist
```plist
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <!-- The Mac App Store requires you specify if the app uses encryption. -->
    <!-- Please consult https://developer.apple.com/documentation/bundleresources/information_property_list/itsappusesnonexemptencryption -->
    <!-- <key>ITSAppUsesNonExemptEncryption</key> -->
    <!-- Please indicate <true/> or <false/> here. -->

    <!-- Specify the category for your app here. -->
    <!-- Please consult https://developer.apple.com/documentation/bundleresources/information_property_list/lsapplicationcategorytype -->
    <!-- <key>LSApplicationCategoryType</key> -->
    <!-- <string>public.app-category.YOUR-CATEGORY-HERE</string> -->
    <key>UIDeviceFamily</key>
    <array>
        <integer>2</integer>
    </array>
    <key>UIRequiredDeviceCapabilities</key>
    <array>
        <string>arm64</string>
    </array>
    <key>UISupportedInterfaceOrientations</key>
    <array>
        <string>UIInterfaceOrientationPortrait</string>
        <string>UIInterfaceOrientationLandscapeLeft</string>
        <string>UIInterfaceOrientationLandscapeRight</string>
    </array>
    <key>UISupportedInterfaceOrientations~ipad</key>
    <array>
        <string>UIInterfaceOrientationPortrait</string>
        <string>UIInterfaceOrientationPortraitUpsideDown</string>
        <string>UIInterfaceOrientationLandscapeLeft</string>
        <string>UIInterfaceOrientationLandscapeRight</string>
    </array>
    <key>XSAppIconAssets</key>
    <string>Assets.xcassets/appicon.appiconset</string>
</dict>
</plist>

```

## Platforms/MacCatalyst/Program.cs
```cs
﻿using ObjCRuntime;
using UIKit;

namespace create4care
{
    public class Program
    {
        // This is the main entry point of the application.
        static void Main(string[] args)
        {
            // if you want to use a different Application Delegate class from "AppDelegate"
            // you can specify it here.
            UIApplication.Main(args, null, typeof(AppDelegate));
        }
    }
}
```

## Platforms/Tizen/Main.cs
```cs
using System;
using Microsoft.Maui;
using Microsoft.Maui.Hosting;

namespace create4care
{
    internal class Program : MauiApplication
    {
        protected override MauiApp CreateMauiApp() => MauiProgram.CreateMauiApp();

        static void Main(string[] args)
        {
            var app = new Program();
            app.Run(args);
        }
    }
}

```

## Platforms/Tizen/tizen-manifest.xml
```xml
﻿<?xml version="1.0" encoding="utf-8"?>
<manifest package="maui-application-id-placeholder" version="0.0.0" api-version="9" xmlns="http://tizen.org/ns/packages">
  <profile name="common" />
  <ui-application appid="maui-application-id-placeholder" exec="create4care.dll" multiple="false" nodisplay="false" taskmanage="true" type="dotnet" launch_mode="single">
    <label>maui-application-title-placeholder</label>
    <icon>maui-appicon-placeholder</icon>
    <metadata key="http://tizen.org/metadata/prefer_dotnet_aot" value="true" />
  </ui-application>
  <shortcut-list />
  <privileges>
    <privilege>http://tizen.org/privilege/internet</privilege>
  </privileges> 
  <dependencies />
  <provides-appdefined-privileges />
</manifest>
```

## Platforms/Windows/App.xaml
```xaml
﻿<maui:MauiWinUIApplication
    x:Class="create4care.WinUI.App"
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
    xmlns:maui="using:Microsoft.Maui"
    xmlns:local="using:create4care.WinUI">

</maui:MauiWinUIApplication>

```

## Platforms/Windows/App.xaml.cs
```cs
﻿using Microsoft.UI.Xaml;

// To learn more about WinUI, the WinUI project structure,
// and more about our project templates, see: http://aka.ms/winui-project-info.

namespace create4care.WinUI
{
    /// <summary>
    /// Provides application-specific behavior to supplement the default Application class.
    /// </summary>
    public partial class App : MauiWinUIApplication
    {
        /// <summary>
        /// Initializes the singleton application object.  This is the first line of authored code
        /// executed, and as such is the logical equivalent of main() or WinMain().
        /// </summary>
        public App()
        {
            this.InitializeComponent();
        }

        protected override MauiApp CreateMauiApp() => MauiProgram.CreateMauiApp();
    }

}

```

## Platforms/Windows/Package.appxmanifest
```appxmanifest
﻿<?xml version="1.0" encoding="utf-8"?>
<Package
  xmlns="http://schemas.microsoft.com/appx/manifest/foundation/windows10"
  xmlns:uap="http://schemas.microsoft.com/appx/manifest/uap/windows10"
  xmlns:mp="http://schemas.microsoft.com/appx/2014/phone/manifest"
  xmlns:rescap="http://schemas.microsoft.com/appx/manifest/foundation/windows10/restrictedcapabilities"
  IgnorableNamespaces="uap rescap">

  <Identity Name="maui-package-name-placeholder" Publisher="CN=User Name" Version="0.0.0.0" />

  <mp:PhoneIdentity PhoneProductId="5EB7DE5A-477A-469D-8EB6-6EDCB07F4EA4" PhonePublisherId="00000000-0000-0000-0000-000000000000"/>

  <Properties>
    <DisplayName>$placeholder$</DisplayName>
    <PublisherDisplayName>User Name</PublisherDisplayName>
    <Logo>$placeholder$.png</Logo>
  </Properties>

  <Dependencies>
    <TargetDeviceFamily Name="Windows.Universal" MinVersion="10.0.17763.0" MaxVersionTested="10.0.19041.0" />
    <TargetDeviceFamily Name="Windows.Desktop" MinVersion="10.0.17763.0" MaxVersionTested="10.0.19041.0" />
  </Dependencies>

  <Resources>
    <Resource Language="x-generate" />
  </Resources>

  <Applications>
    <Application Id="App" Executable="$targetnametoken$.exe" EntryPoint="$targetentrypoint$">
      <uap:VisualElements
        DisplayName="$placeholder$"
        Description="$placeholder$"
        Square150x150Logo="$placeholder$.png"
        Square44x44Logo="$placeholder$.png"
        BackgroundColor="transparent">
        <uap:DefaultTile Square71x71Logo="$placeholder$.png" Wide310x150Logo="$placeholder$.png" Square310x310Logo="$placeholder$.png" />
        <uap:SplashScreen Image="$placeholder$.png" />
      </uap:VisualElements>
    </Application>
  </Applications>

  <Capabilities>
    <rescap:Capability Name="runFullTrust" />
  </Capabilities>

</Package>

```

## Platforms/Windows/app.manifest
```manifest
<?xml version="1.0" encoding="utf-8"?>
<assembly manifestVersion="1.0" xmlns="urn:schemas-microsoft-com:asm.v1">
  <assemblyIdentity version="1.0.0.0" name="create4care.WinUI.app"/>

  <application xmlns="urn:schemas-microsoft-com:asm.v3">
    <windowsSettings>
      <!-- The combination of below two tags have the following effect:
           1) Per-Monitor for >= Windows 10 Anniversary Update
           2) System < Windows 10 Anniversary Update
      -->
      <dpiAware xmlns="http://schemas.microsoft.com/SMI/2005/WindowsSettings">true/PM</dpiAware>
      <dpiAwareness xmlns="http://schemas.microsoft.com/SMI/2016/WindowsSettings">PerMonitorV2, PerMonitor</dpiAwareness>
    </windowsSettings>
  </application>
</assembly>

```

## Platforms/iOS/AppDelegate.cs
```cs
﻿using Foundation;

namespace create4care
{
    [Register("AppDelegate")]
    public class AppDelegate : MauiUIApplicationDelegate
    {
        protected override MauiApp CreateMauiApp() => MauiProgram.CreateMauiApp();
    }
}

```

## Platforms/iOS/Info.plist
```plist
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>LSRequiresIPhoneOS</key>
    <true/>
    <key>UIDeviceFamily</key>
    <array>
        <integer>1</integer>
        <integer>2</integer>
    </array>
    <key>UIRequiredDeviceCapabilities</key>
    <array>
        <string>arm64</string>
    </array>
    <key>UISupportedInterfaceOrientations</key>
    <array>
        <string>UIInterfaceOrientationPortrait</string>
        <string>UIInterfaceOrientationLandscapeLeft</string>
        <string>UIInterfaceOrientationLandscapeRight</string>
    </array>
    <key>UISupportedInterfaceOrientations~ipad</key>
    <array>
        <string>UIInterfaceOrientationPortrait</string>
        <string>UIInterfaceOrientationPortraitUpsideDown</string>
        <string>UIInterfaceOrientationLandscapeLeft</string>
        <string>UIInterfaceOrientationLandscapeRight</string>
    </array>
    <key>XSAppIconAssets</key>
    <string>Assets.xcassets/appicon.appiconset</string>
</dict>
</plist>

```

## Platforms/iOS/Program.cs
```cs
﻿using ObjCRuntime;
using UIKit;

namespace create4care
{
    public class Program
    {
        // This is the main entry point of the application.
        static void Main(string[] args)
        {
            // if you want to use a different Application Delegate class from "AppDelegate"
            // you can specify it here.
            UIApplication.Main(args, null, typeof(AppDelegate));
        }
    }
}

```

## Platforms/iOS/Resources/PrivacyInfo.xcprivacy
```xcprivacy
<?xml version="1.0" encoding="UTF-8"?>
<!--
This is the minimum required version of the Apple Privacy Manifest for .NET MAUI apps.
The contents below are needed because of APIs that are used in the .NET framework and .NET MAUI SDK.

You are responsible for adding extra entries as needed for your application.

More information: https://aka.ms/maui-privacy-manifest
-->
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>NSPrivacyAccessedAPITypes</key>
    <array>
        <dict>
            <key>NSPrivacyAccessedAPIType</key>
            <string>NSPrivacyAccessedAPICategoryFileTimestamp</string>
            <key>NSPrivacyAccessedAPITypeReasons</key>
            <array>
                <string>C617.1</string>
            </array>
        </dict>
        <dict>
            <key>NSPrivacyAccessedAPIType</key>
            <string>NSPrivacyAccessedAPICategorySystemBootTime</string>
            <key>NSPrivacyAccessedAPITypeReasons</key>
            <array>
                <string>35F9.1</string>
            </array>
        </dict>
        <dict>
            <key>NSPrivacyAccessedAPIType</key>
            <string>NSPrivacyAccessedAPICategoryDiskSpace</string>
            <key>NSPrivacyAccessedAPITypeReasons</key>
            <array>
                <string>E174.1</string>
            </array>
        </dict>
        <!--
            The entry below is only needed when you're using the Preferences API in your app.
        <dict>
            <key>NSPrivacyAccessedAPIType</key>
            <string>NSPrivacyAccessedAPICategoryUserDefaults</string>
            <key>NSPrivacyAccessedAPITypeReasons</key>
            <array>
                <string>CA92.1</string>
            </array>
        </dict> -->
    </array>
</dict>
</plist>

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

## Resources/AppIcon/appicon.svg
```svg
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="456" height="456" viewBox="0 0 456 456" version="1.1" xmlns="http://www.w3.org/2000/svg">
    <rect x="0" y="0" width="456" height="456" fill="#512BD4" />
</svg>
```

## Resources/AppIcon/appiconfg.svg
```svg
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="456" height="456" viewBox="0 0 456 456" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" xmlns:serif="http://www.serif.com/" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:2;">
    <path d="m 105.50037,281.60863 c -2.70293,0 -5.00091,-0.90042 -6.893127,-2.70209 -1.892214,-1.84778 -2.837901,-4.04181 -2.837901,-6.58209 0,-2.58722 0.945687,-4.80389 2.837901,-6.65167 1.892217,-1.84778 4.190197,-2.77167 6.893127,-2.77167 2.74819,0 5.06798,0.92389 6.96019,2.77167 1.93749,1.84778 2.90581,4.06445 2.90581,6.65167 0,2.54028 -0.96832,4.73431 -2.90581,6.58209 -1.89221,1.80167 -4.212,2.70209 -6.96019,2.70209 z" style="fill:#ffffff;fill-rule:nonzero;stroke-width:0.838376" />
    <path d="M 213.56111,280.08446 H 195.99044 L 149.69953,207.0544 c -1.17121,-1.84778 -2.14037,-3.76515 -2.90581,-5.75126 h -0.40578 c 0.36051,2.12528 0.54076,6.67515 0.54076,13.6496 v 65.13172 h -15.54349 v -99.36009 h 18.71925 l 44.7374,71.29798 c 1.89222,2.95695 3.1087,4.98917 3.64945,6.09751 h 0.26996 c -0.45021,-2.6325 -0.67573,-7.09015 -0.67573,-13.37293 v -64.02256 h 15.47557 z" style="fill:#ffffff;fill-rule:nonzero;stroke-width:0.838376" />
    <path d="m 289.25134,280.08446 h -54.40052 v -99.36009 h 52.23835 v 13.99669 h -36.15411 v 28.13085 h 33.31621 v 13.9271 h -33.31621 v 29.37835 h 38.31628 z" style="fill:#ffffff;fill-rule:nonzero;stroke-width:0.838376" />
    <path d="M 366.56466,194.72106 H 338.7222 v 85.3634 h -16.08423 v -85.3634 h -27.77455 v -13.99669 h 71.70124 z" style="fill:#ffffff;fill-rule:nonzero;stroke-width:0.838376" />
</svg>
```

## Resources/Fonts/OpenSans-Regular.ttf
```
Error reading file.
```

## Resources/Images/dotnet_bot.svg
```svg
<svg width="419" height="519" viewBox="0 0 419 519" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M284.432 247.568L284.004 221.881C316.359 221.335 340.356 211.735 355.308 193.336C382.408 159.996 372.893 108.183 372.786 107.659L398.013 102.831C398.505 105.432 409.797 167.017 375.237 209.53C355.276 234.093 324.719 246.894 284.432 247.568Z" fill="#8A6FE8"/>
<path d="M331.954 109.36L361.826 134.245C367.145 138.676 375.055 137.959 379.497 132.639C383.928 127.32 383.211 119.41 377.891 114.969L348.019 90.0842C342.7 85.6531 334.79 86.3702 330.348 91.6896C325.917 97.0197 326.634 104.929 331.954 109.36Z" fill="#8A6FE8"/>
<path d="M407.175 118.062L417.92 94.2263C420.735 87.858 417.856 80.4087 411.488 77.5831C405.12 74.7682 397.67 77.6473 394.845 84.0156L383.831 108.461L407.175 118.062Z" fill="#8A6FE8"/>
<path d="M401.363 105.175L401.234 69.117C401.181 62.1493 395.498 56.541 388.53 56.5945C381.562 56.648 375.954 62.3313 376.007 69.2989L376.018 96.11L401.363 105.175Z" fill="#8A6FE8"/>
<path d="M386.453 109.071L378.137 73.9548C376.543 67.169 369.757 62.9628 362.971 64.5575C356.185 66.1523 351.979 72.938 353.574 79.7237L362.04 115.482L386.453 109.071Z" fill="#8A6FE8"/>
<path d="M381.776 142.261C396.359 142.261 408.181 130.44 408.181 115.857C408.181 101.274 396.359 89.4527 381.776 89.4527C367.194 89.4527 355.372 101.274 355.372 115.857C355.372 130.44 367.194 142.261 381.776 142.261Z" fill="url(#paint0_radial)"/>
<path d="M248.267 406.979C248.513 384.727 245.345 339.561 222.376 301.736L199.922 315.372C220.76 349.675 222.323 389.715 221.841 407.182C221.798 408.627 235.263 409.933 248.267 406.979Z" fill="url(#paint1_linear)"/>
<path d="M221.841 406.936L242.637 406.84L262.052 518.065L220.311 518.258C217.132 518.269 214.724 515.711 214.938 512.532L221.841 406.936Z" fill="#522CD5"/>
<path d="M306.566 488.814C310.173 491.661 310.109 495.782 309.831 500.127L308.964 513.452C308.803 515.839 306.727 517.798 304.34 517.809L260.832 518.012C258.125 518.023 256.08 515.839 256.262 513.142L256.551 499.335C256.883 494.315 255.192 492.474 251.307 487.744C244.649 479.663 224.967 435.62 226.84 406.925L248.256 406.829C249.691 423.858 272.167 461.682 306.566 488.814Z" fill="url(#paint2_linear)"/>
<path d="M309.82 500.127C310.023 497.088 310.077 494.176 308.889 491.715L254.635 491.961C256.134 494.166 256.765 496.092 256.562 499.314L256.273 513.121C256.091 515.828 258.146 518.012 260.843 517.99L304.34 517.798C306.727 517.787 308.803 515.828 308.964 513.442L309.82 500.127Z" fill="url(#paint3_radial)"/>
<path d="M133.552 407.471C133.103 385.22 135.864 340.021 158.49 301.993L181.073 315.425C160.545 349.921 159.346 389.972 159.989 407.428C160.042 408.884 146.578 410.318 133.552 407.471Z" fill="url(#paint4_linear)"/>
<path d="M110.798 497.152C110.765 494.187 111.204 491.575 112.457 487.23C131.882 434.132 133.52 407.364 133.52 407.364L159.999 407.246C159.999 407.246 161.819 433.512 181.716 486.427C183.289 490.195 183.471 493.641 183.674 496.831L183.792 513.816C183.803 516.374 181.716 518.483 179.158 518.494L177.873 518.504L116.781 518.782L115.496 518.793C112.927 518.804 110.83 516.728 110.819 514.159L110.798 497.152Z" fill="url(#paint5_linear)"/>
<path d="M110.798 497.152C110.798 496.67 110.808 496.199 110.83 495.739C110.969 494.262 111.643 492.603 114.875 492.582L180.207 492.282C182.561 492.367 183.343 494.176 183.589 495.311C183.621 495.814 183.664 496.328 183.696 496.82L183.813 513.806C183.824 515.411 183.011 516.824 181.769 517.669C181.031 518.172 180.132 518.472 179.179 518.483L177.895 518.494L116.802 518.772L115.528 518.782C114.244 518.793 113.077 518.269 112.232 517.434C111.386 516.599 110.862 515.432 110.851 514.148L110.798 497.152Z" fill="url(#paint6_radial)"/>
<path d="M314.979 246.348C324.162 210.407 318.008 181.777 318.008 181.777L326.452 181.734L326.656 181.574C314.262 115.75 256.326 66.0987 186.949 66.4198C108.796 66.773 45.7233 130.424 46.0765 208.577C46.4297 286.731 110.08 349.803 188.234 349.45C249.905 349.172 302.178 309.474 321.304 254.343C321.872 251.999 321.797 247.804 314.979 246.348Z" fill="url(#paint7_radial)"/>
<path d="M310.237 279.035L65.877 280.148C71.3998 289.428 77.95 298.012 85.3672 305.761L290.972 304.829C298.336 297.005 304.8 288.368 310.237 279.035Z" fill="#D8CFF7"/>
<path d="M235.062 312.794L280.924 312.585L280.74 272.021L234.877 272.23L235.062 312.794Z" fill="#512BD4"/>
<path d="M243.001 297.626C242.691 297.626 242.434 297.53 242.22 297.327C242.006 297.123 241.899 296.866 241.899 296.588C241.899 296.299 242.006 296.042 242.22 295.839C242.434 295.625 242.691 295.528 243.001 295.528C243.312 295.528 243.568 295.635 243.782 295.839C243.996 296.042 244.114 296.299 244.114 296.588C244.114 296.877 244.007 297.123 243.793 297.327C243.568 297.519 243.312 297.626 243.001 297.626Z" fill="white"/>
<path d="M255.192 297.434H253.212L247.967 289.203C247.839 289 247.721 288.775 247.636 288.55H247.593C247.636 288.786 247.657 289.299 247.657 290.091L247.668 297.444H245.912L245.891 286.228H247.999L253.062 294.265C253.276 294.597 253.415 294.833 253.479 294.95H253.511C253.458 294.651 253.437 294.148 253.437 293.441L253.426 286.217H255.17L255.192 297.434Z" fill="white"/>
<path d="M263.733 297.412L257.589 297.423L257.568 286.206L263.465 286.195V287.779L259.387 287.79L259.398 290.969L263.155 290.958V292.532L259.398 292.542L259.409 295.86L263.733 295.85V297.412Z" fill="white"/>
<path d="M272.445 287.758L269.298 287.769L269.32 297.401H267.5L267.479 287.769L264.343 287.779V286.195L272.434 286.174L272.445 287.758Z" fill="white"/>
<path d="M315.279 246.337C324.355 210.836 318.457 182.483 318.308 181.798L171.484 182.462C171.484 182.462 162.226 181.563 162.268 190.018C162.311 198.463 162.761 222.341 162.878 248.746C162.9 254.172 167.363 256.773 170.863 256.751C170.874 256.751 311.618 252.213 315.279 246.337Z" fill="url(#paint8_radial)"/>
<path d="M227.685 246.798C227.685 246.798 250.183 228.827 254.571 225.499C258.959 222.17 262.812 221.977 266.869 225.445C270.925 228.913 293.616 246.498 293.616 246.498L227.685 246.798Z" fill="#A08BE8"/>
<path d="M320.748 256.141C320.748 256.141 324.943 248.414 315.279 246.348C315.289 246.305 170.927 246.894 170.927 246.894C167.566 246.905 163.232 244.925 162.846 241.671C162.857 244.004 162.878 246.369 162.889 248.756C162.91 253.68 166.582 256.27 169.878 256.698C170.21 256.73 170.542 256.773 170.874 256.773L180.742 256.73L320.748 256.141Z" fill="#512BD4"/>
<path d="M206.4 233.214C212.511 233.095 217.302 224.667 217.102 214.39C216.901 204.112 211.785 195.878 205.674 195.997C199.563 196.116 194.772 204.544 194.973 214.821C195.173 225.099 200.289 233.333 206.4 233.214Z" fill="#512BD4"/>
<path d="M306.249 214.267C306.356 203.989 301.488 195.605 295.377 195.541C289.266 195.478 284.225 203.758 284.118 214.037C284.011 224.315 288.878 232.699 294.99 232.763C301.101 232.826 306.142 224.545 306.249 214.267Z" fill="#512BD4"/>
<path d="M205.905 205.291C208.152 203.022 211.192 202.016 214.157 202.262C215.912 205.495 217.014 209.733 217.111 214.389C217.164 217.3 216.811 220.04 216.158 222.513C212.669 223.519 208.752 222.662 205.979 219.922C201.912 215.909 201.88 209.348 205.905 205.291Z" fill="#8065E0"/>
<path d="M294.996 204.285C297.255 202.016 300.294 200.999 303.259 201.256C305.164 204.628 306.309 209.209 306.256 214.239C306.224 216.808 305.892 219.259 305.303 221.485C301.793 222.523 297.843 221.678 295.061 218.916C291.004 214.892 290.972 208.342 294.996 204.285Z" fill="#8065E0"/>
<path d="M11.6342 357.017C10.9171 354.716 -5.72611 300.141 21.3204 258.903C36.9468 235.078 63.3083 221.035 99.6664 217.15L102.449 243.276C74.3431 246.273 54.4676 256.345 43.3579 273.202C23.0971 303.941 36.5722 348.733 36.7113 349.183L11.6342 357.017Z" fill="url(#paint9_linear)"/>
<path d="M95.1498 252.802C109.502 252.802 121.137 241.167 121.137 226.815C121.137 212.463 109.502 200.828 95.1498 200.828C80.7976 200.828 69.1628 212.463 69.1628 226.815C69.1628 241.167 80.7976 252.802 95.1498 252.802Z" fill="url(#paint10_radial)"/>
<path d="M72.0098 334.434L33.4683 329.307C26.597 328.397 20.2929 333.214 19.3725 340.085C18.4627 346.956 23.279 353.26 30.1504 354.181L68.6919 359.308C75.5632 360.217 81.8673 355.401 82.7878 348.53C83.6975 341.658 78.8705 335.344 72.0098 334.434Z" fill="#8A6FE8"/>
<path d="M3.73535 367.185L7.35297 393.076C8.36975 399.968 14.7702 404.731 21.6629 403.725C28.5556 402.708 33.3185 396.308 32.3124 389.415L28.5984 362.861L3.73535 367.185Z" fill="#8A6FE8"/>
<path d="M15.5194 374.988L34.849 405.427C38.6058 411.292 46.4082 413.005 52.2735 409.248C58.1387 405.491 59.8512 397.689 56.0945 391.823L41.7953 369.144L15.5194 374.988Z" fill="#8A6FE8"/>
<path d="M26.0511 363.739L51.8026 389.019C56.7688 393.911 64.7532 393.846 69.6445 388.88C74.5358 383.914 74.4715 375.929 69.516 371.038L43.2937 345.297L26.0511 363.739Z" fill="#8A6FE8"/>
<path d="M26.4043 381.912C40.987 381.912 52.8086 370.091 52.8086 355.508C52.8086 340.925 40.987 329.104 26.4043 329.104C11.8216 329.104 0 340.925 0 355.508C0 370.091 11.8216 381.912 26.4043 381.912Z" fill="url(#paint11_radial)"/>
<path d="M184.73 63.6308L157.819 66.5892L158.561 38.5412L177.888 36.4178L184.73 63.6308Z" fill="#8A6FE8"/>
<path d="M170.018 41.647C180.455 39.521 187.193 29.3363 185.067 18.8988C182.941 8.46126 172.757 1.72345 162.319 3.84944C151.882 5.97543 145.144 16.1601 147.27 26.5976C149.396 37.0351 159.58 43.773 170.018 41.647Z" fill="#D8CFF7"/>
<path d="M196.885 79.385C198.102 79.2464 198.948 78.091 198.684 76.8997C195.851 64.2818 183.923 55.5375 170.773 56.9926C157.622 58.4371 147.886 69.5735 147.865 82.4995C147.863 83.7232 148.949 84.6597 150.168 84.5316L196.885 79.385Z" fill="url(#paint12_radial)"/>
<defs>
<radialGradient id="paint0_radial" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(382.004 103.457) scale(26.4058)">
<stop stop-color="#8065E0"/>
<stop offset="1" stop-color="#512BD4"/>
</radialGradient>
<linearGradient id="paint1_linear" x1="214.439" y1="303.482" x2="236.702" y2="409.505" gradientUnits="userSpaceOnUse">
<stop stop-color="#522CD5"/>
<stop offset="0.4397" stop-color="#8A6FE8"/>
</linearGradient>
<linearGradient id="paint2_linear" x1="231.673" y1="404.144" x2="297.805" y2="522.048" gradientUnits="userSpaceOnUse">
<stop stop-color="#522CD5"/>
<stop offset="0.4397" stop-color="#8A6FE8"/>
</linearGradient>
<radialGradient id="paint3_radial" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(280.957 469.555) rotate(-0.260742) scale(45.8326)">
<stop offset="0.034" stop-color="#522CD5"/>
<stop offset="0.9955" stop-color="#8A6FE8"/>
</radialGradient>
<linearGradient id="paint4_linear" x1="166.061" y1="303.491" x2="144.763" y2="409.709" gradientUnits="userSpaceOnUse">
<stop stop-color="#522CD5"/>
<stop offset="0.4397" stop-color="#8A6FE8"/>
</linearGradient>
<linearGradient id="paint5_linear" x1="146.739" y1="407.302" x2="147.246" y2="518.627" gradientUnits="userSpaceOnUse">
<stop stop-color="#522CD5"/>
<stop offset="0.4397" stop-color="#8A6FE8"/>
</linearGradient>
<radialGradient id="paint6_radial" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(148.63 470.023) rotate(179.739) scale(50.2476)">
<stop offset="0.034" stop-color="#522CD5"/>
<stop offset="0.9955" stop-color="#8A6FE8"/>
</radialGradient>
<radialGradient id="paint7_radial" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(219.219 153.929) rotate(179.739) scale(140.935)">
<stop offset="0.4744" stop-color="#A08BE8"/>
<stop offset="0.8618" stop-color="#8065E0"/>
</radialGradient>
<radialGradient id="paint8_radial" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(314.861 158.738) rotate(179.739) scale(146.053)">
<stop offset="0.0933" stop-color="#E1DFDD"/>
<stop offset="0.6573" stop-color="white"/>
</radialGradient>
<linearGradient id="paint9_linear" x1="54.1846" y1="217.159" x2="54.1846" y2="357.022" gradientUnits="userSpaceOnUse">
<stop offset="0.3344" stop-color="#9780E6"/>
<stop offset="0.8488" stop-color="#8A6FE8"/>
</linearGradient>
<radialGradient id="paint10_radial" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(90.3494 218.071) rotate(-0.260742) scale(25.9924)">
<stop stop-color="#8065E0"/>
<stop offset="1" stop-color="#512BD4"/>
</radialGradient>
<radialGradient id="paint11_radial" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(25.805 345.043) scale(26.4106)">
<stop stop-color="#8065E0"/>
<stop offset="1" stop-color="#512BD4"/>
</radialGradient>
<radialGradient id="paint12_radial" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(169.113 67.3662) rotate(-32.2025) scale(21.0773)">
<stop stop-color="#8065E0"/>
<stop offset="1" stop-color="#512BD4"/>
</radialGradient>
</defs>
</svg>

```

## Resources/Images/step_1.png
```
Error reading file.
```

## Resources/Images/step_2.png
```
Error reading file.
```

## Resources/Images/step_3.png
```
Error reading file.
```

## Resources/Images/step_4.png
```
Error reading file.
```

## Resources/Images/step_5.png
```
Error reading file.
```

## Resources/Raw/AboutAssets.txt
```txt
﻿Any raw assets you want to be deployed with your application can be placed in
this directory (and child directories). Deployment of the asset to your application
is automatically handled by the following `MauiAsset` Build Action within your `.csproj`.

    <MauiAsset Include="Resources\Raw\**" LogicalName="%(RecursiveDir)%(Filename)%(Extension)" />

These files will be deployed with your package and will be accessible using Essentials:

    async Task LoadMauiAsset()
    {
        using var stream = await FileSystem.OpenAppPackageFileAsync("AboutAssets.txt");
        using var reader = new StreamReader(stream);

        var contents = reader.ReadToEnd();
    }

```

## Resources/Splash/splash.svg
```svg
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="456" height="456" viewBox="0 0 456 456" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" xmlns:serif="http://www.serif.com/" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:2;">
    <path d="m 105.50037,281.60863 c -2.70293,0 -5.00091,-0.90042 -6.893127,-2.70209 -1.892214,-1.84778 -2.837901,-4.04181 -2.837901,-6.58209 0,-2.58722 0.945687,-4.80389 2.837901,-6.65167 1.892217,-1.84778 4.190197,-2.77167 6.893127,-2.77167 2.74819,0 5.06798,0.92389 6.96019,2.77167 1.93749,1.84778 2.90581,4.06445 2.90581,6.65167 0,2.54028 -0.96832,4.73431 -2.90581,6.58209 -1.89221,1.80167 -4.212,2.70209 -6.96019,2.70209 z" style="fill:#ffffff;fill-rule:nonzero;stroke-width:0.838376" />
    <path d="M 213.56111,280.08446 H 195.99044 L 149.69953,207.0544 c -1.17121,-1.84778 -2.14037,-3.76515 -2.90581,-5.75126 h -0.40578 c 0.36051,2.12528 0.54076,6.67515 0.54076,13.6496 v 65.13172 h -15.54349 v -99.36009 h 18.71925 l 44.7374,71.29798 c 1.89222,2.95695 3.1087,4.98917 3.64945,6.09751 h 0.26996 c -0.45021,-2.6325 -0.67573,-7.09015 -0.67573,-13.37293 v -64.02256 h 15.47557 z" style="fill:#ffffff;fill-rule:nonzero;stroke-width:0.838376" />
    <path d="m 289.25134,280.08446 h -54.40052 v -99.36009 h 52.23835 v 13.99669 h -36.15411 v 28.13085 h 33.31621 v 13.9271 h -33.31621 v 29.37835 h 38.31628 z" style="fill:#ffffff;fill-rule:nonzero;stroke-width:0.838376" />
    <path d="M 366.56466,194.72106 H 338.7222 v 85.3634 h -16.08423 v -85.3634 h -27.77455 v -13.99669 h 71.70124 z" style="fill:#ffffff;fill-rule:nonzero;stroke-width:0.838376" />
</svg>
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
        <PackageReference Include="Microsoft.Maui.Controls" Version="$(MauiVersion)" />
        <PackageReference Include="Microsoft.AspNetCore.Components.WebView.Maui" Version="$(MauiVersion)" />
        <PackageReference Include="Microsoft.Extensions.Logging.Debug" Version="9.0.0" />
        <PackageReference Include="Plugin.BLE" Version="3.2.0-beta.1" />
    </ItemGroup>

</Project>

```

## create4care.csproj.user
```user
﻿<?xml version="1.0" encoding="utf-8"?>
<Project ToolsVersion="Current" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <PropertyGroup>
    <ActiveDebugFramework>net9.0-windows10.0.19041.0</ActiveDebugFramework>
    <IsFirstTimeProjectOpen>False</IsFirstTimeProjectOpen>
    <ActiveDebugProfile>Windows Machine</ActiveDebugProfile>
  </PropertyGroup>
</Project>
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
    --clr-text-rev: #E8E8E8;
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
        --clr-text-rev: #171717;
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
        <link rel="icon" href="data:,">

        <!-- Chart Scripts -->
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        
        <!-- MediaPipe Scripts -->
        <script src="https://cdn.jsdelivr.net/npm/@mediapipe/control_utils/control_utils.js" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/@mediapipe/drawing_utils/drawing_utils.js" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/@mediapipe/pose/pose.js" crossorigin="anonymous"></script>
        
        <!-- Your custom JS for starting MediaPipe Pose -->
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
