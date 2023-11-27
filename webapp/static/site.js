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
    var difference = results + " .difference";

    props = ['Population','Median_Age','Average_Income','Percent_High_School','Percent_Bachelors','Housing_Units_Total',
    'Housing_Units_Single_Family','Percent_In_Poverty','Food_Services_Employers','Waste_Management_Employers',
    'Arts_Employers','Education_Employers','Finance_Employers','Healthcare_Employers','Information_Employers',
    'Technical_Employers','Real_Estate_Employers','Retail_Employers','Transportation_Employers','Utilities_Employers'];

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
            
            for (p in props)
            {
                field = props[p]
                value = parsed_place[field]
                output += "<div class='form-row'>";
                output += "<input type='text' id='txt_" + field + "' class='txt_" + field + "' value='" + value + "'>";
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
        var popValue = jQuery(predictForm + " .txt_Population").val();
        var medianAgeValue = jQuery(predictForm + " .txt_Median_Age").val();
        var avgIncomeValue = jQuery(predictForm + " .txt_Average_Income").val();
        var perHighSchoolValue = jQuery(predictForm + " .txt_Percent_High_School").val();
        var perBachValue = jQuery(predictForm + " .txt_Percent_Bachelors").val();
        var housingTotalValue = jQuery(predictForm + " .txt_Housing_Units_Total").val();
        var housingSingleValue = jQuery(predictForm + " .txt_Housing_Units_Single_Family").val();
        var perPovertyValue = jQuery(predictForm + " .txt_Percent_In_Poverty").val();
        var foodEmpValue = jQuery(predictForm + " .txt_Food_Services_Employers").val();
        var wasteEmpValue = jQuery(predictForm + " .txt_Waste_Management_Employers").val();
        var artsEmpValue = jQuery(predictForm + " .txt_Arts_Employers").val();
        var edEmpValue = jQuery(predictForm + " .txt_Education_Employers").val();
        var finEmpValue = jQuery(predictForm + " .txt_Finance_Employers").val();
        var healthEmpValue = jQuery(predictForm + " .txt_Healthcare_Employers").val();
        var infoEmpValue = jQuery(predictForm + " .txt_Information_Employers").val();
        var techEmpValue = jQuery(predictForm + " .txt_Technical_Employers").val();
        var reEmpValue = jQuery(predictForm + " .txt_Real_Estate_Employers").val();
        var retailEmpValue = jQuery(predictForm + " .txt_Retail_Employers").val();
        var transEmpValue = jQuery(predictForm + " .txt_Transportation_Employers").val();
        var utilityEmpValue = jQuery(predictForm + " .txt_Utilities_Employers").val();
        
        jQuery(progressIndicator).show();
        
        jQuery.post(
            jQuery(predictForm).attr("action"),
            {
                geoid: geoidValue,
                population: popValue,
                medianage: medianAgeValue,
                avgincome: avgIncomeValue,
                perhighschool: perHighSchoolValue,
                perbach: perBachValue,
                housingtotal: housingTotalValue,
                housingsingle: housingSingleValue,
                perpoverty: perPovertyValue,
                foodemp: foodEmpValue,
                wasteemp: wasteEmpValue,
                artsemp: artsEmpValue,
                edemp: edEmpValue,
                finemp: finEmpValue,
                healthemp: healthEmpValue,
                infoemp: infoEmpValue,
                techemp: techEmpValue,
                reemp: reEmpValue,
                retailemp: retailEmpValue,
                transemp: transEmpValue,
                utilityemp: utilityEmpValue
            }
        ).done(function (r)
        {
            jQuery(progressIndicator).hide();
            
            jQuery(actual).text(r.actual)
            jQuery(prediction).text(r.prediction)
            jQuery(difference).text(r.difference + "%")
        });
    }    
});