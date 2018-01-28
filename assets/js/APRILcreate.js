//Create.js - TF2 Tags Item Creation Handler

var step = 1;
var set = false;
var error = false;
var itemCount = 1;

// Adjust for April
var APRIL = true;
var NUM_CLASSES = 11;
var NUM_SLOTS   = 17;

var finalClass = "";
var finalSlot = "";
var finalBase = "";
var finalImage = "";
var finalName = "";
var finalDesc = "";
var finalPrefix = "";
var finalFilter = "";
var finalColor = "FFD700";
var finalPaint = "";
var finalParticles = "";
var finalStyle = "";
//var finalKeywords = "";

var item = null;
var paintable = false;
var item_data = null;

function getCookie(name)
{
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
 
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
 
$.ajaxSetup({
    beforeSend: function(xhr, settings) {        
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

$(document).ready(function (){
    for (var x = 1; x <= NUM_CLASSES; x++)
    {
        $('#class'+x).click(function() {
            classSelect($(this).attr('classname'));
        });
    }
    
    for (var x = 0; x <= NUM_SLOTS; x++)
    {
        $('#slot'+x).click(function() {
            slotSelect($(this).attr('slotname'));
        });
    }
    
    $('#name').click(function () {
        if ($(this).val() == finalBase)
            $(this).select();
    });
    
    $('#nameItem').click(function() {
        nameItem();
    });
        
    $('#editName').click(function() {
        resetAdvanced();
        setItem(finalImage);
    });
        
    $('input[name=advoption]').click(function(){
        hideAdvanced();
        if ($(this).val() == 'particle' /*&& finalPrefix == "Unusual" APRIL*/)
        {
            if (finalBase == "The Horseless Headless Horsemann's Headtaker")
                return false;
            $('#particles').show();
        }
        if (($(this).val() == 'paint') && (item_data["paintable"] == true))
        {
            $('#paint').show();
        }
        if ($(this).val() == 'rarity')
            $('#rarity').show();
        if ($(this).val() == 'style')
            $('#style').show();
    });
	
	$('#confirm').click(function(){
		$('#step1').hide();
		$('#step2').hide();
		hidesteps();
		addItem();
        
        if (error)
        {
            $('#addAnother').click();
            $('#step1').show();
            $('#step2').show();
            $('#error').show()
        }
        else
        {
            $('#step6').show();
            $('#stepnum').html('Step Six');
            $('#stepdir').html('Your item is ready to submit! You may optionally leave some comma separated keywords here to help others find it easier in the future.');
        }
	});
    
    $('#addAnother').click(function(){
        $('#addAnother').val("Add More Items");
        set = true;
        addItem();
        $('#step2').hide();
        hidesteps();
        step = 1;
        $('#stepnum').html('Step One');
		$('#stepdir').html('Choose a class whose item you wish to name.');
    });
    
    $('img[name=setIconButton]').click(function (){
        token = $(this).data('icon');
        $('input[name=setIcon]').val(token);
        $('#setImage').attr('src', '/assets/items/'+token+'.png');
    });
    
    $('#form').submit(function (e){
        if (! submit_form())
        {
            e.preventDefault();
            return false;
        }
    });
});

function classSelect(classname)
{
    resetItem();
    if (step == 1)
    {
        for (var x = 0; x <= NUM_CLASSES; x++)
        {
            img = $('#class'+x).attr('src');
            if ((img === undefined) || (img.lastIndexOf('sm.png') != -1))
                continue;
            image = img.substring(0, img.lastIndexOf('.')) + "sm.png"
            $('#class'+x).attr('src', image.toLowerCase());
        }
    }
    step = 2;
    finalClass = classname;
    hidesteps();
    $('#step2').show();
    $('#stepnum').html('Step Two');
    $('#stepdir').html('Choose the slot of the item you wish to name.');
    if (APRIL)
    {
        $("#step2 img").each(function (){
            if (finalClass == "April")
            {
                if ($(this).hasClass("april"))
                    $(this).show();
                else
                    $(this).hide();
            }
            else
            {
                if ($(this).hasClass("april"))
                    $(this).hide();
                else
                    $(this).show();
            }
        });
    }
}

function slotSelect(slotname)
{
    resetItem();
    if (step == 2)
    {
        for (var x = 0; x < NUM_SLOTS; x++)
        {
            img = $('#slot'+x).attr('src');
            if ((img === undefined) || (img.lastIndexOf('sm.png') != -1))
                continue;
            image = img.substring(0, img.lastIndexOf('.')) + "sm.png"
            $('#slot'+x).attr('src', image);
        }
    }
    step = 3;
    
    finalSlot = slotname;
    hidesteps();
    $('#step3').show();
    $('#stepnum').html('Step Three');
    $('#stepdir').html('Choose the item you wish to name.');
    
    getItems(finalClass, finalSlot)
}

function getItems(finalClass, finalSlot)
{
    $('#step3').html("");
    ajax_url = '/ajax/getItems?role='+finalClass+'&slot='+finalSlot;
    $.ajax({
        async: false,
        url: ajax_url,
        success: function(data) {
            data = render_item_list(data);
            $('#step3').html(data);
            
            $('.item').click(function() {
                setItem($(this).data('defindex'));
            });
            
            $('#step3').show();
        }
    });
}

function setItem(defindex)
{
    finalImage = defindex;
    finalBase = $('#item-'+defindex).html();
    var image = $('#image-'+defindex).attr('src');
    step = 4;
    hidesteps();
    $('#step4').show();
    $('#stepnum').html('Step Four');
    $('#stepdir').html('Edit the name and/or description of the item.');
    
    $('#img1').attr('src', image)
    $('#name').val(finalBase);
    $('#desc').val('');
}

function hidesteps()
{
    for (var x = 3; x < 7; x++)
        $('#step'+x).hide();
}

function nameItem()
{
    //Make sure you named the item
    if ($('#name').val() == finalBase && $('#desc').val() == "")
    {
        $('#nameError').html("<span class='tf2 strange'>No custom name/desc given!</span>");
        return false;
    }
    else
    {
        $('#nameError').html("");
    }
    finalName = $('#name').val();
    finalDesc = $('#desc').val();
    finalPrefix = "";
    finalColor = "FFD700";
    finalPaint = "";
    finalParticle = "";
    finalStyle = "";
    
    // Hide Advanced Options to prevent clicking invalid data before AJAX returns
    $('#rarity').hide();
    $('#filters').hide();
    $('#filterlist').hide();
    $('#particles').hide();
    $('#paint').hide();
    $('#style').hide();

    //Create Advanced Options
    $.ajax({
        sync: false,
        url: "/ajax/getItem/"+finalImage,
        success: function(data) {
            // Data
            item_data = data;
            populateRarities(data)
            populateParticles(data);
            populateStyles(data["style"]);
            
            // Bindings
            $('div[name=rarity]').click(function() {
                setRarity($(this).text(), $(this).css('color'));
            });
            
            $('div[name=particles]').click(function() {
                setParticles($(this).children("span[name=particle_choice]").html());
                $("html, body").scrollTop($('#step5').offset().top)
            });
            
            $('div[name=paint]').hover(function() {
                pcolor = $(this).attr('color');
                pname = $(this).attr('paint');
                $('#paintCan').attr('src', '/assets/images/paints/'+pcolor+'.png')
                $('#paintName').html(pname);
            });
            
            $('div[name=paint]').click(function() {
                setPaint($(this).attr('color'));
            });
            
            $('div[name=style]').click(function() {
                setStyle($(this).attr('num'));
            });
            
            $('#filters').click(function() {
                showFilters();
            });
            
            $('div[name=filter]').click(function() {
                setFilter($(this).html());
            });
        }
    });

    step = 5;
    hidesteps();
    renderItem();
    $('#step5').show();
    $('#stepnum').html('Step Five');
    $('#stepdir').html('Your item is ready for submission! Adjust any necessary options then hit "Confirm".');
}

function renderItem()
{
    //Headtaker patch
    if (finalBase == "The Horseless Headless Horsemann's Headtaker")
    {
        finalPrefix = "Unusual";
        finalColor= "8650AC";
    }
    
    // Botkiller patch
    if (finalBase.indexOf("Botkiller") != -1)
    {
        finalColor = "CF6A32";
        if (finalPrefix == "" || finalPrefix == "Unique")
            finalPrefix = "Strange";
    }
    
    //Set color
    $('span[name=finalColor]:first').css('color', "#"+finalColor);
    
    //Set name/desc
    if (finalName == finalBase)
        $('span[name=finalName]:first').html(finalName);
    else
        $('span[name=finalName]:first').html('"' + finalName + '"');
    if (finalDesc != "")
        $('span[name=finalDesc]:first').html('"' + finalDesc + '"');
    else
        $('span[name=finalDesc]:first').html(finalDesc);
    
    //Set prefix and filter
    if (finalName == finalBase)
    {
        $('span[name=finalPrefix]:first').html(finalPrefix + " ");
        //Drop the 'the'
        if (finalName.substr(0,4) == "The " && (finalPrefix != ""))
        {
            $('span[name=finalName]:first').html(finalBase.substr(4));
        }
        
        $('span[name=finalFilter]:first').html(finalFilter);
    }
    else
        $('span[name=finalPrefix]:first').html('');
    
    //Particles
    if (finalParticles != "")
    {
        $('span[name=finalParticles]:first').html("Effect: " + finalParticles);
        $('.itemLeft:first').css('background-image', 'url("/assets/images/particles/'+finalParticles+'.png")');
    }
    else
    {
        $('span[name=finalParticles]:first').html('');
        $('.itemLeft:first').css('background-image', '');
    }
    
    //Image
    image = finalImage;
    if (finalPaint != "")
        image += "/"+finalPaint;
    if (finalStyle != "")
        image += "-"+finalStyle;
    
    $('img[name=finalImage]:first').attr('src', '/assets/items/'+image+".png");
    
}

function render_item_list(data)
{
    var out = "";
    var letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"];
    var found_letters = [];
    var letter_links = "<div style='text-align:center'>";
    for (var x = 0; x < data.length; x++)
    {
        var starts_with = data[x]["item_name"].replace("The ", "").toUpperCase().substring(0,1);
        if ($.inArray(starts_with, letters) == -1)
            found_letters.push(starts_with);
        out += '<div class="item" data-defindex="'+data[x]["defindex"]+'" data-starts_with="'+starts_with+'"><img id="image-'+data[x]["defindex"]+'" src="'+data[x]["image"]+'"><div id="item-'+data[x]["defindex"]+'">'+data[x]["item_name"]+'</div></div>\n';
    }
    if (out == "")
    {
        out = "<div class='tf2 Unique' style='text-align:center;font-size:24px;'>No " + finalClass + " " + finalSlot + " items were found</div>";
        return out;
    }
    
    // Create letter links -- LATER
    /*
    for (var x = 0; x < letters.length; x++)
    {
        console.log(letters[letter]);
        if ($.inArray(letters[x], found_letters) != -1)
            letter_links += "<span class='jsLink tf2 Unique' name='letter_link'>"+letters[x]+"</span> ";
        else
            letter_links += "<span class='tf2 Normal'>"+letters[x]+"</span> \n";
    }
    */
    
    return letter_links + "</div>\n" + out;
}

function hideAdvanced()
{
    $('#rarity').hide();
    $('#filterList').hide();
    $('#particles').hide();
    $('#paint').hide();
    $('#style').hide();
}

function populateRarities(item)
{
    var text = "";
    for (var x = 0; x < item["rarities"].length; x++)
    {
        if (x >= 12 && x % 10 == 0) // APRIL
                text += "</div><div class='column' style='text-align:left'>\n"; // APRIL
        text += "<div name='rarity' class='"+rarity_classes[item["rarities"][x]]+"'>" + item["rarities"][x] + "</div>";
    }
    $('#def_rarities').html(text);
    
    text = "";
    if ($.inArray("Strange", item["rarities"]) != -1)
    {
        if (finalSlot == "misc")
            var strange_levels = rarities_cosmetic;
        else if (finalBase == "The Holiday Punch")
            var strange_levels = rarities_holiday_punch;
        else if (finalBase == "The Mantreads")
            var strange_levels = rarities_mantreads;
        else if (finalBase == "Sapper")
            var strange_levels = rarities_sapper;
        else if (finalBase == "The Spirit of Giving")
            var strange_levels = rarities_spirit_of_giving;
        else
            var strange_levels = rarities_strange;
            
        text = "<div class='column'>";
        for (var x = 0; x < strange_levels.length; x++)
        {
            if (x >= 10 && x % 10 == 0)
                text += "</div><div class='column'>\n";
            text += "<div name='rarity' class='Strange'>" + strange_levels[x] + "</div>\n";
        }
        text += "</div>";
    }
    //$('#strange_rarities').html(text); // APRIL
    
    return text;
}

function populateParticles(item)
{
    /* DISABLED FOR APRIL
    if ($.inArray("Unusual", item["rarities"]) == -1)
        $('#particles').html("");
    END APRIL */
        
    text = "";
    for (var x = 0; x < particles.length; x++)
    {
        text += '<div name="particles"><img src="/assets/images/particles/'+particles[x]+'.png"><br><span name="particle_choice">'+particles[x]+'</span></div>';
    }
    $('#particles').html(text);
}

function populateStyles(styles)
{
    text = "";
    for (var x = 0; x < styles.length; x++)
    {
        text += '<div class="tf2" name="style" num="'+x+'">'+styles[x]+'</div>';
    }
    $('#style').html(text);
}

function setRarity(rarity, color)
{
    color = rgb2hex(color)
    if (rarity == "Unique")
        rarity = "";
        
    if (rarity =="Collector")
        rarity = "Collector's";
    
    //Particles
    if (rarity == "Self-Made" || rarity == "Community")
        finalParticles = "Community Sparkle";
    else if (rarity == "Unusual" && finalPrefix != "Unusual")
        finalParticles = "Blizzardy Storm";
    else if (rarity == "Valve")
        finalParticles = "Flying Bits";
    else
        finalParticles = "";
        
    // Show the filter if a strange is selected (It's much easier to check this by color)
    if (color == 'cf6a32')
    {
        $('#filters').show();
    }
    else
    {
        $('#filters').hide();
        $('#filterList').hide();
        $('#strange_rarities').show();
        finalFilter = "";
    }
 
    // Strangified cosmetics
    if (finalPrefix == rarity) // Click twice to force strange rarity/color
    {
        finalPrefix = rarity;
        finalColor = color;
    }
    else if ((finalSlot == "head" || finalSlot == "misc") && color == 'cf6a32' && finalPrefix != "") // Strange rarity/odd color
    {
        //if (finalPrefix == "Strange")
            //finalColor = color;
        finalPrefix = rarity;
    }
    else // Standard rarity/color
    {
        finalPrefix = rarity;
        finalColor = color;
    }
    
    
    renderItem();
}

function setParticles(particles)
{
    finalParticles = particles;
    renderItem();
}

function setPaint(color)
{
    if (color == "blank")
        finalPaint = "";
    else
        finalPaint = color;
    renderItem();
}

function setStyle(num)
{
    if (num == 0)
        finalStyle = "";
    else
        finalStyle = num;
    renderItem();
}

function resetItem()
{
    finalBase = "";
    finalImage = "";
    finalName = "";
    finalDesc = "";
    resetAdvanced();
}

function resetAdvanced()
{
    finalPrefix = "";
    finalFilter = "";
    finalColor = "FFD700";
    finalPaint = "";
    finalParticles = "";
    finalStyle = "";
    
    $('.itemLeft:first').css('background-image', '');
}

function addItem()
{
	$('#error').hide();
    text = "<span class='debug'>";
	
    /*
    text += 'CLASS: <input name="finalClass" value="'+finalClass+'"><br>';
	text += 'SLOT: <input name="finalSlot" value="'+finalSlot+'"><br>';
	text += 'BASE: <input name="finalBase" value="'+finalBase+'"><br>';
	text += 'IMAGE: <input name="finalImage" value="'+finalImage+'"><br>';
    text += 'NAME: <input name="finalName" value=""><br>';
	text += 'DESC: <input name="finalDesc" value=""><br>';
	text += 'PREFIX: <input name="finalPrefix" value="'+finalPrefix+'"><br>';
    text += 'FILTER: <input name="finalFilter" value="'+finalFilter+'"><br>';
	text += 'COLOR: <input name="finalColor" value="'+finalColor+'"><br>';
	text += 'PAINT: <input name="finalPaint" value="'+finalPaint+'"><br>';
	text += 'PARTICLE: <input name="finalParticle" value="'+finalParticles+'"><br>';
	text += 'STYLE: <input name="finalStyle" value="'+finalStyle+'"><br>';
    */
    
    // JSON-ize
    
    var j = {};
    j.defindex  = parseInt(finalImage);
    j.role      = finalClass;
    j.slot      = finalSlot;
    j.base      = finalBase;
    j.name      = finalName;
    j.desc      = finalDesc;
    j.prefix    = finalPrefix;
    j.filter    = finalFilter;
    j.color     = finalColor;
    j.paint     = finalPaint;
    j.particles = finalParticles;
    j.style     = finalStyle;
    
    json = JSON.stringify(j);
    
    // Pre-submission verify
    $.ajax({
        async: false,
        type: "POST",
        url: "/ajax/verify",
        data: {"json":json},
        success: function(data) {   
            if (data == "SUCCESS")
            {
                text += 'JSON: <input name="json" value="'+encodeURIComponent(json)+'"><br></span>';
                
                wip = $('#wip');
                wip = wip.removeAttr('id');
                $('#setOverview').append("<div class='setContainer' id='item"+itemCount+"'><div class='setItem'>"+wip.html()+text+"</div><div class='setPosition'><input type='button' class='tf2button narrow' name='upButton' value='&#9650;'><br><br><input type='button' class='tf2button narrow' name='removeButton' value='X' data-number='"+itemCount+"'><br><br><input type='button' class='tf2button narrow' name='downButton' value='&#9660;'></div></div>");
                wip.attr("id", "wip");
                
                // Quotation marks inserted like that don't escape properly, this should work around it.
                $('input[name=finalName]:last').val(finalName);
                $('input[name=finalDesc]:last').val(finalDesc);
                
                if (set)
                {
                    $('#setOverview').show();
                    $('#setSettings').show();
                    $('.setContainer').show();
                }
                
                itemCount += 1;
                error = false;
                $("input[type=submit]").removeAttr("disabled");
                $("input[type=submit]").val("Submit My Creation");
            }
            else
            {
                $('#error').show();
                $('#error_txt').val(data + "\n\nRaw Data:\n" + json);
                error = true;
                $("input[type=submit]").attr("disabled", "disabled");
                $("input[type=submit]").val("Sorry, try again.");
            }
        }
    });
    
	finalClass = "";
	finalSlot = "";
	finalBase = "";
	finalImage = "";
	finalName = "";
	finalDesc = "";
	finalPrefix = "";
    fianalFilter = "";
	finalColor = "FFD700";
	finalPaint = "";
	finalParticles = "";
	finalStyle = "";
    
    setEditBindings();
}

function rgb2hex(rgb) {
     if (  rgb.search("rgb") == -1 ) {
          return rgb;
     } else {
          rgb = rgb.match(/^rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*(\d+))?\)$/);
          function hex(x) {
               return ("0" + parseInt(x).toString(16)).slice(-2);
          }
          return hex(rgb[1]) + hex(rgb[2]) + hex(rgb[3]); 
     }
}

function showFilters()
{
    $('#strange_rarities').hide();
    $('#filterList').show();
}

function setFilter(value)
{
    if (value == "None")
    {
        finalFilter = "";
        renderItem();
        return true;
    }
    finalFilter = value;
    renderItem();
}

function setEditBindings()
{
    $('input[name=removeButton]').click(function (){
        remove = $(this).data('number');
        $('#item'+remove).remove();
        setEditBindings();
    });

    $('input[name=upButton]').click(function (){
        origin = $(this).parent().parent();
        originID = origin.attr('id');
        originHtml = origin.html();
        
        destination = origin.prev();
        destinationID = destination.attr('id');
        destinationHtml = destination.html();
        
        if (destinationHtml != null)
        {
            $('#'+originID).html(destinationHtml);
            $('#'+destinationID).html(originHtml);
        }
        
        setEditBindings();
    });   
    
    $('input[name=downButton]').click(function (){
        origin = $(this).parent().parent();
        originID = origin.attr('id');
        originHtml = origin.html();
        
        destination = origin.next();
        destinationID = destination.attr('id');
        destinationHtml = destination.html();
        
        if (destinationHtml != null)
        {
            $('#'+originID).html(destinationHtml);
            $('#'+destinationID).html(originHtml);
        }
        
        setEditBindings();
    });   
}

function submit_form()
{
    var submission = {
        "items": [],
        "meta": {
            "keywords": $('textarea[name=finalKeywords]').val(),
            "set_name": $('input[name=setName]').val(),
            "set_icon": $('input[name=setIcon]').val(),
        }
    };
    $('input[name=json]').each(function (){
        submission["items"].push($.parseJSON(decodeURIComponent($(this).val())));
    });
    
    $('#submission').val(JSON.stringify(submission));
    return true;
}