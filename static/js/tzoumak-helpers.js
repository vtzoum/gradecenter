////////////////////////////
// Call as document.getElementsByTagName("button")[0].addEventListener("click",    beep);
////////////////////////////
function beep() {
    var snd = new  Audio("data:audio/wav;base64,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qJrx4KOQjahZxWbcZgztj2c49nKmkId44S71j0c8eV9yDK6uPRzx5X18eDvjvQ6yKo9ZSS6l//8elePK/Lf//IInrOF/FvDoADYAGBMGb7FtErm5MXMlmPAJQVgWta7Zx2go+8xJ0UiCb8LHHdftWyLJE0QIAIsI+UbXu67dZMjmgDGCGl1H+vpF4NSDckSIkk7Vd+sxEhBQMRU8j/12UIRhzSaUdQ+rQU5kGeFxm+hb1oh6pWWmv3uvmReDl0UnvtapVaIzo1jZbf/pD6ElLqSX+rUmOQNpJFa/r+sa4e/pBlAABoAAAAA3CUgShLdGIxsY7AUABPRrgCABdDuQ5GC7DqPQCgbbJUAoRSUj+NIEig0YfyWUho1VBBBA//uQZB4ABZx5zfMakeAAAAmwAAAAF5F3P0w9GtAAACfAAAAAwLhMDmAYWMgVEG1U0FIGCBgXBXAtfMH10000EEEEEECUBYln03TTTdNBDZopopYvrTTdNa325mImNg3TTPV9q3pmY0xoO6bv3r00y+IDGid/9aaaZTGMuj9mpu9Mpio1dXrr5HERTZSmqU36A3CumzN/9Robv/Xx4v9ijkSRSNLQhAWumap82WRSBUqXStV/YcS+XVLnSS+WLDroqArFkMEsAS+eWmrUzrO0oEmE40RlMZ5+ODIkAyKAGUwZ3mVKmcamcJnMW26MRPgUw6j+LkhyHGVGYjSUUKNpuJUQoOIAyDvEyG8S5yfK6dhZc0Tx1KI/gviKL6qvvFs1+bWtaz58uUNnryq6kt5RzOCkPWlVqVX2a/EEBUdU1KrXLf40GoiiFXK///qpoiDXrOgqDR38JB0bw7SoL+ZB9o1RCkQjQ2CBYZKd/+VJxZRRZlqSkKiws0WFxUyCwsKiMy7hUVFhIaCrNQsKkTIsLivwKKigsj8XYlwt/WKi2N4d//uQRCSAAjURNIHpMZBGYiaQPSYyAAABLAAAAAAAACWAAAAApUF/Mg+0aohSIRobBAsMlO//Kk4soosy1JSFRYWaLC4qZBYWFRGZdwqKiwkNBVmoWFSJkWFxX4FFRQWR+LsS4W/rFRb/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////VEFHAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAU291bmRib3kuZGUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMjAwNGh0dHA6Ly93d3cuc291bmRib3kuZGUAAAAAAAAAACU=");  
    snd.play();
}



////////////////////////////
// JQXWIDGET Widget Look and Feel
////////////////////////////
var theme = 'bootstrap';    
//  custom custom-bootstrap custom-darkblue
// Arctic,  Black, Bootstrap, Energy Blue, Fresh,  Dark Blue
// Orange , Summer , 'Web Classic'
// Metro , Office 'Metro Dark' 'Shiny Black' 'High Contrast'
var height = '400px'; 
var width = '100%';

////////////////////////////
//DJANGO_MESSAGES in JSON Responses
////////////////////////////
function helperAjaxMessagesProcess() {

    $(document).ajaxComplete(function (e, xhr, settings) {
        var contentType = xhr.getResponseHeader("Content-Type");
        if (contentType == "application/javascript" || contentType == "application/json") {
            //var json = $.evalJSON(xhr.responseText);
            var json = $.parseJSON(xhr.responseText);
            $.each(json.django_messages, function (i, item) {
                //helperAddMessage1(item.message, item.extra_tags);
                helperAddMessageDIV(item.message, item.extra_tags);
            });

        }
    }).ajaxError(function (e, xhr, settings, exception) {
        //helperAddMessage1("There was an error processing your request, please try again.", "error");
        //addMessage("There was an error processing your request, please try again.", "error");
        helperAddMessageDIV("There was an error processing your request, please try again.", "error");
    })

}
/*
function helperAjaxMessagesProcess(response) {
    // Handle Booking.POST Request messages
    $.each(response.django_messages, function (i, item) {
        helperAddMessageDIV(item.message, item.extra_tags);
    });
}
*/
function helperAddMessageDIV(text, extra_tags) {
    
    //var message = $('<li class="'+extra_tags+'">'+text+'</li>').hide();
    var html = '<div id="alertBox" class="alert fresh-color alert-'+ extra_tags +' alert-dismissible" role="alert">';
    html = html + '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">×</span></button>'
    html = html + '<span id="alertBoxMessage"><strong>!&nbsp;&nbsp;</strong>'+ text +'</span>'
    html = html + '</div>'
    var message = $(html)
    $("#jsonMessages").append(message); 
    message.fadeIn(500);
    if (extra_tags=="error") {
        beep();
        //console.log("Error");
    };
    setTimeout(function() {
        message.fadeOut(500, function() {
            message.remove();
        });
    }, 3000);
    /*
    */
}


//Original FUnction
function helperAddMessage(text, extra_tags) {
    var message = $('<li class="'+extra_tags+'">'+text+'</li>').hide();
    $("#messages").append(message);
    message.fadeIn(500);

    setTimeout(function() {
        message.fadeOut(500, function() {
            message.remove();
        });
    }, 3000);

    //console.log (text);
    
}

//Original FUnction
/*
function helperAddMessage1(text, extra_tags) {
    var message = $('
        <div class="alert alert-dismissable alert-${extra_tags}">\n
            <a class="close" data-dismiss="alert" href="#">&times;</a>\n
                ${text}\n
        </div>').hide();
    $("#messages").append(message);
    message.fadeIn(500);

    setTimeout(function() {
        message.fadeOut(500, function() {
            message.remove();
        });
    }, 3000);
}        
*/

////////////////////////////
// Data Arrays-Lists
////////////////////////////
var ArrayLetterCode= [];
ArrayLetterCode[0]= {id:0, code:'Επιστολή Α0'};
ArrayLetterCode[1]= {id:1, code:'Επιστολή Α1'};


var ArrayLessonStatus = [];
ArrayLessonStatus[0]= 'Idle';
ArrayLessonStatus[1]= 'Prepare Accepting';
ArrayLessonStatus[2]= 'Start Accepting';
ArrayLessonStatus[3]= 'Check Accepting';
ArrayLessonStatus[4]= 'Complete Accepting';
ArrayLessonStatus[5]= 'Prepare Grading';
ArrayLessonStatus[6]= 'Start Grading';
ArrayLessonStatus[7]= 'Check Grading';
ArrayLessonStatus[8]= 'Complete Grading';

var ArrayLessonStatus2 = [];
ArrayLessonStatus2[0]= 'ΑΡΧΗ';
ArrayLessonStatus2[1]= 'Παραλαβή-ΠΡΟ';
ArrayLessonStatus2[2]= 'Παραλαβή-ΈNAΡΞΗ';
ArrayLessonStatus2[3]= 'Παραλαβή-ΈΛΕΓΧΟΣ';
ArrayLessonStatus2[4]= 'Παραλαβή-ΤΕΛΟΣ';
ArrayLessonStatus2[5]= 'Βαθμολόγηση-ΠΡΟ';
ArrayLessonStatus2[6]= 'Βαθμολ/ση-ΈNAΡΞΗ';
ArrayLessonStatus2[7]= 'Βαθμολ/ση-ΈΛΕΓΧΟΣ';
ArrayLessonStatus2[8]= 'Βαθμολόγηση-ΤΕΛΟΣ';

////////////////////////////
//Function to get a url based on user.info
//Used mainly in ajax-json views thah fetch data to jqxwidgets
////////////////////////////
function helperGetAjaxLinkForUser (theProperty, theUrl) {
    //var theProperty = "{{user.user.is_active}}";
    if (theProperty) {
        return theUrl; 
    }
    else {
        alert('Unauthorized action!');
        return '/';
    }
    //return "{% if djangoUserIsActive %}theUrl{% else %}'/'{% endif %}";
}


////////////////////////////
//DataProcess: 'GroupBy' a list of elements
//var array = ['Car', 'Car', 'Truck', 'Boat', 'Truck'];
// GroupBy { Car   : 2, Truck : 2, Boat  : 1}
////////////////////////////
//var theArray = [ 'Car', 'Car', 'Truck', 'Boat', 'Truck' ];
function helperDataArrayGroupBy (theArray ) {
    var hist = {};
    theArray.map( function (a) { if (a in hist) hist[a] ++; else hist[a] = 1; } );
    //console.log(hist);
    return hist;
}


// same version but ALSO builds Array on the fly from Adapter
function helperDataArrayGroupByAdapter ( dataAdapter, field ) {   
    var records = dataAdapter.records;
    var hist = {};
    for ( i=0; i < records.length; i++) {
        a = records[i].lexStatus;
        if (a in hist) hist[a] ++; else hist[a] = 1; 
    } //for
    return hist;
}

/*
// same version but ALSO builds Array on the fly from Adapter
function helperDataArrayGroupByAdapterLabelValue ( dataAdapter ) {   
    var records = dataAdapter.records;
    var keys = {};
    var hist = {};
    for ( i=0; i < records.length; i++) {
        a = records[i].ddeName;
        if (a in hist) {
            hist.push({ label: a, value: 1, });
            hist[a][value]=++; 
            hist[a][value]=++; 
        } 
        else {
            hist.push({ label: a, value: 1, });
        }
    } //for
    return hist;
}
*/
////////////////////////////
// jqxGRID helpers for EDIT Column
////////////////////////////
//var that = this;
function helperGridInlineEdit(gridId, row, event) {
    that.editrow = row;
    $(gridId).jqxGrid('beginrowedit', row);
    if (event) {
        if (event.preventDefault) {
            event.preventDefault();
        }
    }
    return false;
}

function helperGridInlineUpdate(gridId, row, event) {
    that.editrow = -1;
    $(gridId).jqxGrid('endrowedit', row);
    if (event) {
        if (event.preventDefault) {
            event.preventDefault();
        }
    }
    return false;
}

function helperGridInlineCancel(gridId, row, event) {
    that.editrow = -1;
    $(gridId).jqxGrid('endrowedit', row, true);
    if (event) {
        if (event.preventDefault) {
            event.preventDefault();
        }
    }
    return false;
}


function helperGridInlineEditRenderer (gridId, row, column, value) {
    var eventName = "onclick";
    if (row === that.editrow) {    
    // var vis-edit = 'Edit'; vis-update = 'Update'; vis-cancel = 'Cancel'; 
    // var vis-edit = 'Edit'; vis-update = 'Update'; vis-cancel = 'Cancel'; 
    var visEdit = "<span class='glyphicon glyphicon-edit' aria-hidden='true'></span>";
    var visUpdate = "<span class='glyphicon glyphicon-ok' aria-hidden='true' style='font-size:1.3em;' ></span>";
    var visCancel = "<span class='glyphicon glyphicon-remove' aria-hidden='true' style='font-size:1.3em;' ></span>";
    var gridId = gridId  ; //var gridId = "#grid"; 
    return "<div style='text-align: center; width: 100%; top: 7px; position: relative;'><a " + eventName + "='helperGridInlineUpdate(" + '"' + gridId + '",' + row + ", event)' style='color: inherit;' href='javascript:;'>"+visUpdate+"</a><span style=''>/</span>" + "<a " + eventName + "='helperGridInlineCancel(" + '"' + gridId + '",' + row + ", event)' style='color: inherit;' href='javascript:;'>"+visCancel+"</a></div>";
    }

    return "<div style='text-align: center; width: 100%; top: 7px; position: relative;'><a " + eventName + "='helperGridInlineEdit(" + '"' + gridId + '",' + row + ", event)' style='color: inherit; href='javascript:;'><span class='glyphicon glyphicon-edit large' aria-hidden='true' style='font-size:1.5em;' ></span></a></div>";
    //return "<a " + eventName + "='Edit(" + row + ", event)' style='color: inherit; margin-left: 50%; left: -15px; top: 7px; position: relative;' href='javascript:;'>Edit</a>";
    
    /*
    return "<div style='text-align: center; width: 100%; top: 7px; position: relative;'><a " + eventName + "='helperGridInlineUpdate(" +'"#grid",' + row + ", event)' style='color: inherit;' href='javascript:;'>"+visUpdate+"</a><span style=''>/</span>" + "<a " + eventName + "='helperGridInlineCancel(" +'"#grid",' + row + ", event)' style='color: inherit;' href='javascript:;'>"+visCancel+"</a></div>";
                    }
                return "<div style='text-align: center; width: 100%; top: 7px; position: relative;'><a " + eventName + "='helperGridInlineEdit(" +'"#grid",' + row + ", event)' style='color: inherit; href='javascript:;'><span class='glyphicon glyphicon-edit large' aria-hidden='true' style='font-size:1.5em;' ></span></a></div>";
                //return "<a " + eventName + "='Edit(" + row + ", event)' style='color: inherit; margin-left: 50%; left: -15px; top: 7px; position: relative;' href='javascript:;'>Edit</a>";
    */

}

///////////////////////////
// Lesson > Type jqxGrid dropdown column
//////////////////////////                        
// SchoolToGradeType (@ ORM as CHOICES)
// ['ΚΕΝΟ', 'ΗΜΕΡΗΣΙΟ', 'ΕΣΠΕΡΙΝΟ']; OK 
var ArraySchoolToGradeSchoolType = ['ΗΜΕΡΗΣΙΟ', 'ΕΣΠΕΡΙΝΟ'];
//var ArraySchoolToGradeSchoolType = ['ΚΕΝΟ', 'ΗΜΕΡΗΣΙΟ', 'ΕΣΠΕΡΙΝΟ'];
var dataArraySchoolToGradeType = [];
for ( i=0; i < ArraySchoolToGradeSchoolType.length; i++)
    dataArraySchoolToGradeType.push( {type: i, lexType: ArraySchoolToGradeSchoolType[i] } ) ;
//source
var sourceSchoolToGradeType = { datatype: "array", 
    localdata: dataArraySchoolToGradeType, id: 'type',
    datafields: [{ name: 'type' }, { name: 'lexType'}],
}; //source 
var dataAdapterSchoolToGradeType = new $.jqx.dataAdapter(sourceSchoolToGradeType, {autoBind: true});

/*
///////////////////////////
//SchoolToGrade> jqxGrid dropdown column
//////////////////////////                        
// SchoolToGradeType (@ ORM as CHOICES)
// ['ΚΕΝΟ', 'ΗΜΕΡΗΣΙΟ', 'ΕΣΠΕΡΙΝΟ']; OK 
var ArraySchoolToGradeSchoolType = ['ΚΕΝΟ', 'ΗΜΕΡΗΣΙΟ', 'ΕΣΠΕΡΙΝΟ'];
var dataArraySchoolToGradeType = [];
for ( i=0; i < ArraySchoolToGradeSchoolType.length; i++)
    dataArraySchoolToGradeType.push( {type: i, lexType: ArraySchoolToGradeSchoolType[i] } ) ;
var sourceSchoolToGradeType = { datatype: "array", 
    localdata: dataArraySchoolToGradeType,
    datafields: [{ name: 'type' }, { name: 'lexType'}],
}; //source 
var dataAdapterSchoolToGradeType = new $.jqx.dataAdapter(sourceSchoolToGradeType, {autoBind: true});
*/
///////////////////////////
//School jqxGrid dropdown column
//////////////////////////                        
/*
*/
// SchoolType (@ ORM as CHOICES )
// [ 'ΓΥΜΝΑΣΙΟ', 'ΛΥΚΕΙΟ', 'ΙΔΙΩΤΙΚΟ', 'ΑΛΛΟ', ]; OK
var ArraySchoolType = [ 'ΓΥΜΝΑΣΙΟ', 'ΛΥΚΕΙΟ', 'ΙΔΙΩΤΙΚΟ', 'ΑΛΛΟ', ];
var dataArraySchoolType = [];
for ( i=0; i < ArraySchoolType.length; i++)
    dataArraySchoolType.push( {type: i, lexType: ArraySchoolType[i] } ) ;
var sourceSchoolType = { datatype: "array", 
    localdata: dataArraySchoolType,
    datafields: [{ name: 'type' }, { name: 'lexType'}],
}; //source 
var dataAdapterSchoolType = new $.jqx.dataAdapter(sourceSchoolType, {autoBind: true});


///////////////////////////
//BOOKINg jqxGrid dropdown column
//////////////////////////      
// BOOKINg.action
//var ArrayBookingAction = [ 'Χρέωση', 'Παραλαβή', ]; 
var ArrayBookingAction = [ '-->>', '<<--', ]; 
var dataArrayBookingAction = [];
for ( i=0; i < ArrayBookingAction.length; i++)
    dataArrayBookingAction.push( {action: i, lexAction: ArrayBookingAction[i] } ) ;
var sourceBookingAction = { datatype: "array", 
    localdata: dataArrayBookingAction,
    datafields: [{ name: 'action' }, { name: 'lexAction'}],
}; //source 
var dataAdapterBookingAction = new $.jqx.dataAdapter(sourceBookingAction, {autoBind: true});

// BOOKINg.station
var ArrayBookingStation = [ 'Αποθήκη', 'Φύλαξη', ]; 
var dataArrayBookingStation = [];
for ( i=0; i < ArrayBookingStation.length; i++)
    dataArrayBookingStation.push( {station: i, lexStation: ArrayBookingStation[i] } ) ;

var sourceBookingStation = { datatype: "array", 
    localdata: dataArrayBookingStation,
    datafields: [{ name: 'station' }, { name: 'lexStation'}],
}; //source 
var dataAdapterBookingStation = new $.jqx.dataAdapter(sourceBookingStation, {autoBind: true});



///////////////////////////
//FOLDER jqxGrid dropdown column
//////////////////////////                        
// Folder.type(@ ORM as CHOICES )
var ArrayFolderType = ['Φ(Α)', 'Φ(Β)', 'Φ(ΑΝΑ)',]
//var ArrayFolderType = [ 'Κανονικός', 'Αναβαθμολόγηση', ]; 
var dataArrayFolderType = [];
for ( i=0; i < ArrayFolderType.length; i++)
    dataArrayFolderType.push( {codeType: i, lexType: ArrayFolderType[i] } ) ;

var sourceFolderType = { datatype: "array", 
    localdata: dataArrayFolderType,
    datafields: [{ name: 'codeType' }, { name: 'lexType'}],
}; //source 
var dataAdapterFolderType = new $.jqx.dataAdapter(sourceFolderType, {autoBind: true});

//alert(dataAdapterFolderType.records[0].lexType);
//alert(dataAdapterFolderType.records[1].codeType);

// Folder.status(@ ORM as CHOICES )
// [ 'Αχρέωτος', 'Χρεωμένος', 'Χρεωμένος(2η)', 'Επιστροφή', ]; 
var ArrayFolderStatus = [ 'Αχρέωτος', 'Χρεωμένος', 'Ολοκληρώθηκε', ];
//var ArrayFolderStatus = [ 'Αχρέωτος(A)', 'Αχρέωτος(B)', 'Αχρέωτος(C)', 'Χρεωμένος(A)', 'Χρεωμένος(B)', 'Χρεωμένος(C)', 'NULL', 'NULL', 'Επιστροφή', ]; 
var dataArrayFolderStatus = [];
for ( i=0; i < ArrayFolderStatus.length; i++)
    dataArrayFolderStatus.push( {codeStatus: i, lexStatus: ArrayFolderStatus[i] } ) ;
    
var sourceFolderStatus = { datatype: "array", 
    localdata: dataArrayFolderStatus,
    datafields: [{ name: 'codeStatus' }, { name: 'lexStatus'}],
}; //source 
var dataAdapterFolderStatus = new $.jqx.dataAdapter(sourceFolderStatus, {autoBind: true});

// Folder.status(@ ORM as CHOICES )
// LOCATION_TYPE = ( (0, 'Αποθήκη'), (1, 'Βαθμολογητής'), (2, 'Φύλαξη'), )
var ArrayFolderLocation = [ 'Αποθήκη', 'Βαθμολογητής', 'Φύλαξη', ]; 
var dataArrayFolderLocation = [];
for ( i=0; i < ArrayFolderLocation.length; i++)
    dataArrayFolderLocation.push( {codeLocation: i, lexLocation: ArrayFolderLocation[i] } ) ;

var sourceFolderLocation = { datatype: "array", 
    localdata: dataArrayFolderLocation,
    datafields: [{ name: 'codeLocation' }, { name: 'lexLocation'}],
}; //source 
var dataAdapterFolderLocation = new $.jqx.dataAdapter(sourceFolderLocation, {autoBind: true});

// Folder.type(@ ORM as CHOICES )
// [ 'Πράσινο(Α)', 'Κόκκινο(Β)', 'Αναβαθμολόγηση(Γ)', ]; OK
//var ArrayFolderType = [ 'Πράσινο(Α)', 'Κόκκινο(Β)', 'Αναβαθμολόγηση(Γ)', ]; 
// Folder.status(@ ORM as CHOICES )
// [ 'Αχρέωτος(Αποθήκη)', 'Διόρθωση(Βαθμολογητής)', 'Φύλαξη', 'Επιστροφή(Αποθήκη)', 'Τελείωσε(Αποθήκη)', ]; OK
//var ArrayFolderStatus = [ 'Αχρέωτος(Αποθήκη)', 'Διόρθωση(Βαθμολογητής)', 'Φύλαξη', 'Επιστροφή(Αποθήκη)', 'Τελείωσε(Αποθήκη)', ]; 


///////////////////////////
//SCHOOL jqxGrid dropdown column
//////////////////////////                        
// DIDETYPE/NAME(Taken from Table > Field values )
//var ArrayDDETable = [ {code:'230', name: 'Δ/ΝΣΗ Δ.Ε. ΠΕΙΡΑΙΑ'} , {code:'255', name: 'Δ/ΝΣΗ Δ.Ε. ΗΛΕΙΑΣ'} , ]; 
var sourceDDETable = { 
    datatype: "json",
    url: '/dde/data/', 
    //datafields: [{name: "id"}, {name: "name"}, ],
    datafields: [{ name: 'id' }, {name: 'code' }, { name: 'name'}, ],
}; //source 
//var dataAdapterDDETable = new $.jqx.dataAdapter(sourceDDETable, {autoBind: true});
var dataAdapterDDETable = new $.jqx.dataAdapter(sourceDDETable);

///////////////////////////
//TEACHER jqxGrid dropdown column
//////////////////////////                        
//var ArrayDDETable = [ {code:'230', name: 'Δ/ΝΣΗ Δ.Ε. ΠΕΙΡΑΙΑ'} , {code:'255', name: 'Δ/ΝΣΗ Δ.Ε. ΗΛΕΙΑΣ'} , ]; 
var sourceSpecialtyTable = { 
    datatype: "json",
    url: '/specialty/data/', 
    //datafields: [{name: "id"}, {name: "name"}, ],
    datafields: [{ name: 'id' }, {name: 'code' }, { name: 'name'}, ],
}; //source 
//var dataAdapterSpecialtyTable = new $.jqx.dataAdapter(sourceSpecialtyTable, {autoBind: true});
var dataAdapterSpecialtyTable = new $.jqx.dataAdapter(sourceSpecialtyTable);


////////////////////////////
// AJAX FORM Serialize ALL (+disabled) input
////////////////////////////
/*
 * Improved Version
 * Call As below:
 $('button').click(function(){
    var data = $('form').serializeAll();
    alert(data.toSource());
});
*/
 (function ($) {
  $.fn.helperSerializeAll = function () {
    var data = $(this).serializeArray();
          
    $(':disabled[name]', this).each(function () { 
        data.push({ name: this.name, value: $(this).val() });
    });
      
    return data;
  }
})(jQuery);

/*
 * Original Version
(function ($) {
  $.fn.helperSerializeAllArray = function () {
    var obj = {};

    $('input',this).each(function () { 
        obj[this.name] = $(this).val(); 
    });
    return $.param(obj);
  }
})(jQuery);

*/
////////////////////////////
// JQXGRID > Get Checked row ids
////////////////////////////
function helperJqxgridGetSelectedIds (theGrid, theField) {
    
    var rowindexes = $(theGrid).jqxGrid('getselectedrowindexes');
    var values = [];
    $.each(rowindexes, function() {
     var value = $(theGrid).jqxGrid('getcellvalue', this, theField);
     //var value = $(theGrid).jqxGrid('getcellvalue', this, 'id');
     values.push(value);
    });
    //alert('Selected Row Indexes: ' + rowindexes);
    //alert('Selected Values (id): ' + values);
    //$("#jqxinputGraderNewTeacherArray").val(values);   // Lesson.id
    return values;
}

////////////////////////////
// String funcs
////////////////////////////
/**
* stripTags
*
* @param mixed input
* @parm mixed output
*/

//Tested 
function stripStringTags(input) {
    return input.replace(/(<([^>]+)>)/ig,"");
}

//Function to capitalise first character for strings
// Used for (JS) true false => (python) True False
function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}



////////////////////////////
// CHART funcs
////////////////////////////
function unicodeToChar(text) {
   return text.replace(/\\u[\dA-F]{4}/gi,
          function (match) {
               return String.fromCharCode(parseInt(match.replace(/\\u/g, ''), 16));
          });
}


function unicodeEscape(str) {
  return str.replace(/[\s\S]/g, function (escape) {
    return '\\u' + ('0000' + escape.charCodeAt().toString(16)).slice(-4);
  });
}

/**
*
* Create an instance of the BarGauge.
*
* @constructor
* @param {String} id The name from DOM.
* @param {Number} value
* @param {String} color
* @param {String} backgroundColor
* @param {String} title
* @param {String} subtitle
* @param {Boolean} isHalf Determine geometry of the BarGauge.
* @generate {Object} - BarGauge
*/
function generateBarGauge(id, value, color, backgroundColor, title, subtitle, isHalf) 
{
var endValue = getLastNumberFromTitle(title);
isHalf = isHalf || false;
$('#' + id).jqxBarGauge({
    width: "100%",
    height: 300,
    min: 0,
    max: endValue,
    useGradient: false,
    backgroundColor: backgroundColor,
    customColorScheme: {
        name: 'newScheme',
        colors: [color]
    },
    colorScheme: 'newScheme',
    relativeInnerRadius: 0.8,
    geometry: {
        startAngle: isHalf ? 180 : 90,
        endAngle: isHalf ? 0 : 90
    },
    labels: { precision: 0, indent: 10 },
    title: {
        text: title,
        font: { size: 20 },
        verticalAlignment: 'bottom',
        margin: { top: 0, bottom: 5 },
        subtitle: {
            text: subtitle,
            font: { size: 13 }
        }
    },
    values: value
});
} // unction


// changesBarGauge 
var changesBarGauge = function (id, titleText, subtitleText, values)
{
    $('#' + id).jqxBarGauge({
        title: { text: titleText, subtitle: subtitleText },
        values: values
    });
};




//untested 
/*
function strip_tags(input) {
    if (input) {
        var tags = /(]+)>)/ig;
        if (!is_array(input)) {
            input = input.replace(tags,”);
        }
        else {
            var i = input.length;
            var newInput = new Array();
            while(i–) {
                input[i] = input[i].replace(tags,”);
            }
        }
        return input;
    }
return false;
}
*/
////////////////////////////
// workaround to send additional POST data
////////////////////////////
/*
$("#jqxFileUpload").on('uploadStart', function(){
        //CSS3 Selector to retreive the form
        $('form[action="upload.php"]').append('<input type="hidden" name="name" value="value" />');
    });
*/

////////////////////////////
// AJAX
////////////////////////////
//data: {'id':'1'},
//$.getJSON('/jsonfileuploadcsv/', function (data) {console.log(data);}
/*
$.ajax({
    dataType: "json",        
    type: "POST",
    url: "/ajaxformpost/",    
    data: $("#formPost").serialize(),
    //data: { action:"checkimport", jqxinputFileName : 'uploads/LessonsCSV.csv', jqxinputIdxName: 0, jqxinputFirstRow: 1, csrfmiddlewaretoken: csrftoken, }, 
    success: function(response){
        //$("#success").html(response.data);
        //console.log(response.data);
        console.log(response);
        //alert("success");
    },             
    error: function(){
        console.log('error');
    }
});//ajax

$('.get-more').click(function(){
    $.ajax({
        type: "GET",
        url: "/ajax/more/",
        data: { "item": $(".todo-item").val() },
        success: function(data) {
        for(i = 0; i < data.length; i++){
            $('ul').append('<li>'+data[i]+'</li>');
        }
    }
    }); //ajax
});//.get-more'.click

*/

