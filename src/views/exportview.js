/*
  Export View
  
  Initializes the View interface as well as defines properties for the exportview button.

*/

PivotViewer.Views.ExportView = PivotViewer.Views.IPivotViewerView.subClass({
	init: function () {
		this._super();
	},
	Setup: function (width, height, offsetX, offsetY, tileMaxRatio) { 
		this.width = width;
        this.height = height;
        this.offsetX = offsetX;
        this.offsetY = offsetY;
        this.maxRatio = tileMaxRatio;
        this.currentWidth = this.width;
        this.currentHeight = this.height;
        this.currentOffsetX = this.offsetX;
        this.currentOffsetY = this.offsetY;
	},
	Filter: function (dzTiles, currentFilter, sortFacet, stringFacets) {
		var option = 0;
		
		//console.log("First round:", currentFilter, sortFacet, stringFacets);
		
		$('#myModal').modal();
		$('#myModal').on('shown.bs.modal', function () { // dynamically resize modal
		    $(this).find('.modal-dialog').css({width:'auto',
		                               height:'auto', 
		                              'max-height':'100%'});
		});
		$("#rules").addClass("active"); 
		graphs(); // graphs() by default
		
		$( "#rules" ).click(function() {
			$("#rules").addClass("active"); // highlight the rules button
			$("#contr").removeClass("active");
			option = 0;
			console.log("Rules Clicked");
			graphs();
		});
		$( "#contr" ).click(function() {
			$("#rules").removeClass("active");
			option = 1;
			console.log("Graphs Clicked");
			graphs();
		});		
		$( "#anno" ).click(function() {
			option = 2;
		  $("#contr").removeClass("active"); // deselect Contributions
		});

		function graphs() {
			 //console.log(stringFacets)
			// console.log(JSON.stringify(stringFacets[0].facetValue))			
			str_array = [];
			temp_array = [];

			if (stringFacets.length == 0) { //display warning if user didn't select a facet
				$('#calcs').html("<h3><font color='#E80000'>Please select facets from " +
									"up to <i>5</i> different categories on the left-hand side." + 
										"</font>");			
				return;
			} else if (stringFacets.length > 5) { //display warning if too many facets
				$('#calcs').html("<h3><font color='#E80000'>You have selected facets from <i>" +
									+ stringFacets.length + "</i> categories. Please select from up to " +
									"<i>5</i>." + 
										"</font>");		
				return;
			}
			var facets = _.map(stringFacets, function(stringObj){ // facets = array of strings
				var ret = '';
				ret += stringObj.facet+'~';
				_.forEach(stringObj.facetValue, function(val){
					ret += val + '~';
				})
				ret = ret.substring(0, ret.length - 1); // to delete last comma
				return ret;
			})
			var data = {
				'facets' : JSON.stringify(facets),
				'tb_facet' : JSON.stringify(sortFacet),
				'facets_length' : stringFacets.length
			}
			$("#calcs").empty(); 
	        $.ajax({
	               type: 'POST',
	               url: 'http://geodata.sdsc.edu/survey1544/pivotviewer/calcs',
	               dataType:"json",
	               data: data
			}).always(function(data, textStatus, error) {
				//console.log(data);
				switch (option) {
					case 0:
						var big = data.results;
						fa = (1 + (5 * stringFacets.length)); // # of elements in array
						k = 0;
						temp_array = [];
						google.load('visualization', '1', {'packages':['table'], "callback": drawTable});
						      function drawTable() {
						        var data = new google.visualization.DataTable();
						        data.addColumn('string', 'Facet');
						        data.addColumn('string', 'Facet Value');
						        data.addColumn('string', 'Accuracy');
						        data.addColumn('string', 'Respondents');
						        data.addColumn('string', 'Total Respondents');
						        data.addColumn('string', 'Response to');
						        data.addColumn('string', 'Response is');
						        data.addColumn('string', 'Contribution factor');
						        data.addColumn('string', 'Contribution factor(%)');

								for (i = 0; i < big.length/fa; i++) { // determines amount of paragraphs
									for (j = 0; j < fa; j++) { // stores parsed data from server into array
										temp_array[j] = big[k];
										k++;					
									}
									for (b = 0; b < stringFacets.length; b++) {
										data.addRows([
								          [stringFacets[0+b].facet,  String(stringFacets[0+b].facetValue),
										   temp_array[3+5*b], temp_array[1+5*b], temp_array[2+5*b],
									       String(sortFacet), temp_array[0], temp_array[4+5*b], 
										   temp_array[5+5*b]]]);		
									}
								}
						        var table = new google.visualization.Table(document.getElementById('calcs'));
								table.draw(data, { // sort by facet name (Alphabetically)
								    sortColumn: 1,
								    sortAscending: false
								});
						      }
						break;
					case 1:	
						fa = (1 + (5 * stringFacets.length)); // # of elements in array
						k = 0;
						str_array = [];
						temp_array = [];
						str = '';
				
						for (i = 0; i < data.results.length/fa; i++) { // determines amount of paragraphs
							for (j = 0; j < fa; j++) { // stores parsed data from server into array
								temp_array[j] = data.results[k];
								k++;					
							}
							for (b = 0; b < stringFacets.length; b++) {
								if (str_array[b] == null ) str_array[b]=""; // init first element
								str_array[b] += // append meaningful str to array
									"<br>If response to <b>" + stringFacets[0+b].facet + 
									"</b> is <b>" + stringFacets[0+b].facetValue + "</b> then with <b>" +
									temp_array[3+5*b] + "</b> accuracy " + "(<b>" + temp_array[1+5*b] + 
									"</b> out of <b>" + temp_array[2+5*b] + "</b> respondents)," + 
									" we can say that the " + "response to <b>" + String(sortFacet) +
									"</b> is <b>" + temp_array[0] + 
									"</b>, the contribution of this factor to the accuracy is <b>" + 
									temp_array[4+5*b]+ "</b>, or <b>" + temp_array[5+5*b] + "%</b>.<br>";			
							}
						}
						for (i = 0; i < str_array.length; i++) { // convert array to str to display
							str += str_array[i];
						}
						$('#calcs').html(str); // display str on modal
						break;
				}
			}); // end ajax
		}
	},
	GetUI: function () { 
		if (Modernizr.canvas)
            return "";
        else
            return "<div class='pv-viewpanel-unabletodisplay'><h2>Unfortunately this view is unavailable as your browser does not support this functionality.</h2>Please try again with one of the following supported browsers: IE 9+, Chrome 4+, Firefox 2+, Safari 3.1+, iOS Safari 3.2+, Opera 9+<br/><a href='http://caniuse.com/#feat=canvas'>http://caniuse.com/#feat=canvas</a></div>";
	},
	GetButtonImage: function () { 
		return 'images/ExportView.png';
	},
	GetButtonImageSelected: function () { 
		return 'images/ExportViewSelected.png';
	},
	GetViewName: function () { 
		return 'Export View'; 
	},
	Activate: function () { this.isActive = true; },
	Deactivate: function () { this.isActive = false; }
});
