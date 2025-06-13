using Microsoft.AspNetCore.Components;

namespace create4care.Components.Models;

public class MeasuringResult
{
    public required int Distance { get; set; }
    public required string Unit { get; set; }
}