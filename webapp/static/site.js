jQuery.noConflict();

jQuery(document).ready(function ()
{
    //form
    var locationForm = ".location-form";
    var locationFormSubmit = locationForm + " .submit";
    var locationGeoId = locationForm + " .geo-id";
    var locationFormSubmitGeodId = locationForm + " .submit-geoid";
    var predictForm = ".predict-form";
    var predictFormFields = predictForm + " .predict-form-fields"
    var predictFormSubmit = predictForm + " .submit";
    var progressIndicator = ".progress-indicator";
    var results = ".results";
    var actual = results + " .actual";
    var prediction = results + " .prediction";
    var change = results + " .change";
    var difference = results + " .difference";

    jQuery(locationFormSubmit).click(function (e)
    {
        e.preventDefault();

        LookupLocation();
    });

    jQuery(locationFormSubmitGeodId).click(function (e)
    {
        e.preventDefault();

        LoadLocationData();
    });

    jQuery(predictFormSubmit).click(function (e)
    {
        e.preventDefault();

        PredictRevenue();
    });
  
    function LookupLocation()
    {
        var locationValue = jQuery(locationForm + " .location-name").val();
        var locationUrl = jQuery(locationForm).attr("action") + "/" + locationValue;
        
        jQuery(progressIndicator).show();
        
        jQuery.get(
            locationUrl
        ).done(function (r)
        {
            jQuery(progressIndicator).hide();
            
            parsed_places = JSON.parse(r.places);
            
            output = ""
            pos = 0;
            for(var pp in parsed_places)
            {
                attr = ""
                if (pos == 0)
                    attr = "checked"

                p = parsed_places[pp]
                output += "<div class='location-wrap'>";
                output += "<input type='radio' id='geoid-" + pos + "' name='geoid' value='" + p.GeoId + "' " + attr + ">";
                output += "<label for='geoid-" + pos + "'>" + p.Place_Name + ", " + p.State_Abbr + "</label>";
                output += "</div>";
                pos += 1;
            }
            
            jQuery(locationGeoId).html(output);
        });
    }

    function LoadLocationData()
    {
        var geoIdValue = jQuery(locationForm + " input:radio[name='geoid']:checked").val();
        var geoidUrl = jQuery(locationForm).attr("geo-action") + "/" + geoIdValue;
                
        jQuery(progressIndicator).show();
        
        jQuery.get(
            geoidUrl
        ).done(function (r)
        {
            parsed_place = JSON.parse(r.place)[0];

            output = "";
            
            for (field in parsed_place)
            {
                value = parsed_place[field]
                output += "<div class='form-row'>";
                output += "<input type='text' id='txt_" + field + "' class='" + field + "' value='" + value + "'>";
                output += "<label for='txt_" + field + "'>" + field.split("_").join(" ") + "</label>"
                output += "</div>";
            }
            
            jQuery(predictFormFields).html(output);
            
            jQuery(progressIndicator).hide();

            PredictRevenue();
        });
    }

    function PredictRevenue()
    {
        var geoidValue = jQuery(locationForm + " input:radio[name='geoid']:checked").val();
        postData = { geoid: geoidValue }
        
        jQuery(predictFormFields + " input").each(function() 
        {
            fieldName = jQuery(this).attr('class');
            postData[fieldName] = jQuery(this).val();
        });

        jQuery(progressIndicator).show();
        
        jQuery.post(
            jQuery(predictForm).attr("action"),
            postData
        ).done(function (r)
        {
            jQuery(progressIndicator).hide();
            
            jQuery(actual).text(r.actual)
            jQuery(prediction).text(r.prediction)
            jQuery(change).text("$" + r.change)
            jQuery(difference).text(r.difference + "%")
        });
    }    
});