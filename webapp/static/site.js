jQuery.noConflict();

jQuery(document).ready(function ()
{
    //form
    var locationForm = ".location-form";
    var locationFormSubmit = locationForm + " .submit";
    var locationGeoId = locationForm + " .geo-id";
    var locationFormSubmitGeodId = locationForm + " .submit-geoid";
    var predictForm = ".predict-form";
    var predictFormSubmit = predictForm + " .submit";
    var progressIndicator = ".progress-indicator";

    jQuery(locationFormSubmit).click(function (e)
    {
        e.preventDefault();

        LookupLocation();
    });
/*
    jQuery(locationFormSubmitGeodId).click(function (e)
    {
        e.preventDefault();

        CreateConfig();
    });

    jQuery(predictFormSubmit).click(function (e)
    {
        e.preventDefault();

        GetIssuesData();
    });
*/  
    function LookupLocation()
    {
        var locationValue = jQuery(locationForm + " .location-name").val();
        var locationUrl = jQuery(locationForm).attr("action") + "/" + locationValue;
        
        jQuery(progressIndicator).show();
        
        jQuery.post(
            locationUrl
        ).done(function (r)
        {
            jQuery(progressIndicator).hide();
            
            parsed_places = JSON.parse(r.places);
            
            output = ""
            for(var pp in parsed_places)
            {
                p = parsed_places[pp]
                output += "<div class='location-wrap'>";
                output += "<input type='radio' id='location' name='location' value='" + p.GeoId + "'>";
                output += "<label for='location'>" + p.Place_Name + "</label>";
                output += "</div>";
            }
            
            jQuery(locationGeoId).html(output);
        });
    }
/*
    function GetIssuesData()
    {
        var configurationValue = jQuery(issuesForm + " .configuration").val();

        jQuery(pageData).hide();
        jQuery(progressIndicator).show();
        jQuery(histogramWrap).empty();
        jQuery(allocationDataRows).empty();
        jQuery(sprintDataRows).empty();
        
        jQuery.post(
            jQuery(issuesForm).attr("action"),
            {
                configuration: configurationValue
            }
        ).done(function (r)
        {
            if (r.Succeeded)
            {
                DisplayLinks(r.SubtasksCompleteUrl, r.DevPlanUrl);
                DisplayStatistics(r.QACompletion, r.ProjectCompletion, r.PercentOfBudgetUsed, r.HoursRemaining, r.BugToTicketRatio, r.CompletionDate, r.FECompletionDate, r.BECompletionDate);
                DisplayBurn(r.BurnToEstimateRatio, r.BurnToAllocationRatio);
                DisplayRequirements(r.RequirementCompletion, r.FeatureCount, r.UnestimatedFeatureCount, r.UnestimatedUrl, r.BSAAllocation)
                DisplayEstimates(r.FrontendHours, r.FrontendAllocation, r.BackendHours, r.BackendAllocation);
                DisplayAllocations(r.ResourceAllocations);
                DisplayHistogram(r.StatusHistogram);
                DisplaySprintStats(r.SprintStats);
                DisplayRoleStats(r.HoursBurnedByRole);
            }
            jQuery(progressIndicator).hide();
            jQuery(pageData).show();
        });
    }

    function DisplayLinks(subtasksCompleteUrl)
    {
        var output = "";

        output += "<a href='" + subtasksCompleteUrl + "' target='_blank'>View Tickets with Subtasks Complete</a>";
        
        jQuery(projectLinks).html(output);
    }*/
});