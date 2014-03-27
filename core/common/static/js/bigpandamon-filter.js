/***
 * bigpandamon-filter.js
 ***/
/*
var pgst;
var filter;
var shFilter;
var fields;
var tableid;
var datasrc;
//		var colsDict = {};
//		var shFilter = [];
var colsOrig;
var fieldIndices;
	// fake values
//		var fltr = {'pgst': 'ini'};
var fltr;
var stFlag;
	// END fake values
*/

function buildFilterTable(tableid)
{
//    $( "#fSubFrom" ).datetimepicker({ dateFormat: "yy-mm-dd" });
//    $( "#fSubTo" ).datetimepicker({ dateFormat: "yy-mm-dd" });
    $("#btnFilter-" + tableid).show();
}


function gFV(fieldName)
//gFV ... getFieldValue : get value of input with id===fieldName
{
 return $.trim($("#"+fieldName).val());
}
function sFV(fieldName, val)
//sFV ... setFieldValue : set value of input with id===fieldName
{
 $("#"+fieldName).val(val);
}
function sFVms(fieldName, valList)
//sFVms ... setFieldValue : set option selected for multi select
{
 vals = valList.split(',');
 $("#"+fieldName).val(vals);
}

function setValuesFilterTable(f)
//setValuesFilterTable
{
 for (x in f){
     if(f[x].value.indexOf(',') === -1){
         sFV(f[x].name, f[x].value);
     } else {
         sFVms(f[x].name, f[x].value);
     }
 }
}

function getValuesFilterTable(fields)
//getValuesFilterTableHTCondorJob
{
// var fields = ['fOwn', 'fWmsId', 'fGlJobId', 'fSubFrom', 'fSubTo', 'fRunT', 
//               'fSt', 'fStatus', 'fPri']
 var f = [];

 for (i in fields){
     k = fields[i];
     val = gFV(k);
     if(val.length>0){f.push({'name': k, 'value': val}); }
 }
 return f;
}



$.fn.dataTableExt.oApi.fnReloadAjax = function ( oSettings, sNewSource, fnCallback, bStandingRedraw )
{
    if ( typeof sNewSource != 'undefined' && sNewSource != null )
    {
        oSettings.sAjaxSource = sNewSource;
    }
    this.oApi._fnProcessingDisplay( oSettings, true );
    var that = this;
    var iStart = oSettings._iDisplayStart;
 
    this.fnDraw();
}


function upURL(f){
	// upURL -- update URL with filter
//	    f ... filter dictionary
	    var nH = "";
	    for (x in f)
	    {
	        if (x != 0){
	            nH += '&';
	        }
	        nH += encodeURIComponent(f[x].name) + '=' + encodeURIComponent(f[x].value) ;
	    }
	    window.location.hash = nH;
	    console.debug('nH='+nH);
}


function getHashParams() {
	// getHashParams
	    var hashParams = [];
	    var e,
	        a = /\+/g,  // Regex for replacing addition symbol with a space
	        r = /([^&;=]+)=?([^&;]*)/g,
	        d = function (s) { return decodeURIComponent(s.replace(a, " ")); },
	        q = window.location.hash.substring(1);
	    while (e = r.exec(q))
	       hashParams.push({ 'name': d(e[1]), 'value': d(e[2]) });
	    return hashParams;
}

function getFilterURL(){
	// get filter from URL to populate filter table
	    filter = getHashParams();
	    if ( typeof filter != 'undefined' && filter != null ){
	        pgst = 'fltr';
	    } else {
	        pgst = 'ini';
	    }
}

function drawTable(stFlag){
	// nuke old table with old data
	    if ( typeof oTable != 'undefined' && oTable != null ){
	        oTable.fnClearTable();
	    }
	// get filter parameters
	   fltr=getValuesFilterTable(fields);

	// create new table with new data
	    oTable = $("#" + tableid).dataTable( {
			"sPaginationType": "full_numbers",
			"bDestroy": true,
			"aLengthMenu": [ [10, 100, 250, 500, 1000, -1], [10, 100, 250, 500, 1000, "All"] ],
			"sDom": '<"H"lfr><t><"F"ip>',
			"iDisplayLength": 10,
			"bProcessing": true,
			"bServerSide": true,
			"bFilter": false,
			"bPaginate": true,
			"sAjaxSource": datasrc,
			"bScrollCollapse": true,
			"sScrollX": "100%",
			"bJQueryUI": true,
			"fnServerData": function ( sSource, aoData, fnCallback ) {
				aoData.push({'name': 'csrfmiddlewaretoken', 'value': csrftoken});
				aoData.push({'name': 'pgst', 'value': stFlag});
				$.merge( aoData, fltr )
				$.ajax( {
					"dataType": 'json',
					"url": sSource,
					"data": aoData,
					"type": "POST", 
					"success": fnCallback,
					"async":true,
					"error": function (xhr, error, thrown) {
						alert("THERE IS AN ERROR");
						if ( error == "parsererror" ) 
							apprise( "DataTables warning: JSON data" + 
								" from server could not be parsed. " +
								"This is caused by a JSON formatting " +
								"error." 
							);
					}
				} );
			}, 
			"aoColumns": colsOrig, 
			"aoColumnDefs": [
				// produsername + workinggroup
				{
					"mRender": function ( data, type, row ) {
//						var a = '<a href="'
//							+ '{{ prefix }}' 
//							+ Django.url('jobInfo', {'prodUserName': data, 'nhours': 72})
//							+ '" target="_blank">' +
//							data + '</a>' +' / '+ row.workinggroup;
//						return a;
						return data + ' / ' + row.workinggroup;
					},
					"aTargets": [ fieldIndices.produsername ]
				},
				// JEDI Task ID
				{
					"mRender": function ( data, type, row ) {
					// TODO: add link to task page
						return data;
					},
					"aTargets": [ fieldIndices.jeditaskid ]
				},
				// PanDA ID
				{
					"mRender": function ( data, type, row ) {
					var a = '<a href="'
								+ '{{ prefix }}' 
								+ Django.url('jobDetails', {'pandaid': data})
							+ '" target="_blank">' + data + '</a>'
						;
						return a;
					},
					"aTargets": [ fieldIndices.pandaid ]
				},
				// Job status
				{
					"mRender": function ( data, type, row ) {
						if (data === 'failed'){
							var a = 
								'<span style="color:red;">'
								+ data
								+ '</span>';
							return a;
						} else {
							return data;
						};
					},
					"aTargets": [ fieldIndices.jobstatus ]
				},
				// Site+Cloud
				{
					"mRender": function ( data, type, row ) {
					// TODO: add link to site activity page
						return row.cloud + '.'+ data ;
					},
					"aTargets": [ fieldIndices.computingsite ]
				},
				{ "bVisible": false, "aTargets": [ fieldIndices.cloud ] }
			]
		} );

	// update GET parameters
	    upURL(fltr);
	console.debug("end of drawTable");
}

//showFilter({{tableid}}, {{caption}})
function showFilter(tableid, caption){
	console.debug("showFilter: tableid="+ tableid);
	$("#div-table-filter-" + tableid).show();
	$("#div-table-filter-button-" + tableid).show();
	$("#sh-filter-" + tableid).text("Hide filter of " + caption);
}

// hideFilter({{tableid}}, {{caption}})
function hideFilter(tableid, caption){
	console.debug("hideFilter: tableid="+ tableid);
	$("#div-table-filter-" + tableid).hide();
	$("#div-table-filter-button-" + tableid).hide();
	$("#sh-filter-" + tableid).text("Show filter of " + caption);
}

function getColumnTitles()
{
    for (var i=1;i<colsOrig.length; i++ ){
        colsDict[colsOrig[i].mDataProp] = colsOrig[i].sTitle;
    }
}

function gTV(key, tD, dD, colspan, tagType){
    var ret = '<td><b>' + tD[key] + '</b></td><td';
    if(typeof(colspan) != 'undefined')
    {
        cs = colspan * 2 - 1;
        ret += ' colspan=' + cs + ' ';
    }
    ret += '>';
    if (tagType=='a'){
        ret += '<a href="' + dD[key] + '" target="_blank">'+ dD[key] + '</a>';
    } else {
        ret += dD[key];
    }
    ret += '</td>';
    return ret;
}


function fnFormatDetails(tD, dD){
//  fnFormatDetailsHTCondorJob: detail data formatting for HTCondorJob instances
//  args:
//      tD ... titleDict: dictionary with key=field name, value=title
//      dD ... dataDict:  dictionary with key=field name, value=value of the field
//  returns:
//      HTML code of table rows
  return '&nbsp;'
  ;
//+ gTV("p_description", tD, dD, 3)
}

function fnFormatDetails( oTable, nTr )
{
    var oData = oTable.fnGetData( nTr );
    if (Object.keys(colsDict).length === 0){
        getColumnTitles();
    }
    var sOut =
      '<div class="columns">'+
        '<table cellpadding="5" cellspacing="0" border="0">'
    ;
    sOut += fnFormatDetails(colsDict, oData);
    sOut += 
        '</table>'+
      '</div>';
    return sOut;
}

