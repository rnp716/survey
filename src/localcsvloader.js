//
//  HTML5 PivotViewer
//
//  Original Code:
//    Copyright (C) 2011 LobsterPot Solutions - http://www.lobsterpot.com.au/
//    enquiries@lobsterpot.com.au
//
//  Enhancements:
//    Copyright (C) 2012-2014 OpenLink Software - http://www.openlinksw.com/
//
//  This software is licensed under the terms of the
//  GNU General Public License v2 (see COPYING)
//

//CSV loader
PivotViewer.Models.Loaders.LocalCSVLoader = PivotViewer.Models.Loaders.ICollectionLoader.subClass({
    init: function (CSVFile) {
        this.CSVFile = CSVFile;
    },
    LoadCollection: function (collection) {
        var collection = collection;
        this._super(collection);

        var reader = new FileReader();
        reader.onload = function () {

            //collection.CollectionName = $(collectionRoot).attr("Name");
            //collection.BrandImage = $(collectionRoot).attr(namespacePrefix + ":BrandImage") != undefined ? $(collectionRoot).attr(namespacePrefix + ":BrandImage") : "";

            if (data.length <= 1) {
                //Make sure throbber is removed else everyone thinks the app is still running
                $('.pv-loading').remove();

                //Display a message so the user knows something is wrong
                var msg = '';
                msg = msg + 'There are no items in the CSV Collection<br><br>';
                $('.pv-wrapper').append("<div id=\"pv-empty-collection-error\" class=\"pv-modal-dialog\"><div><a href=\"#pv-modal-dialog-close\" title=\"Close\" class=\"pv-modal-dialog-close\">X</a><h2>HTML5 PivotViewer</h2><p>" + msg + "</p></div></div>");
                var t = setTimeout(function () { window.open("#pv-empty-collection-error", "_self") }, 1000)
                return;
            }

            //Categories
            var columns = data[0];
            for (var i = 0; i < columns.length; i++) {
                var column = columns[i];
                var category = new PivotViewer.Models.FacetCategory(column, null, PivotViewer.Models.FacetType.String, true, true, true);
                collection.FacetCategories.push(category);
            }

            //Items
            for (var i = 1; i < data.length; i++) {
                var row = data[0];
                var item = new PivotViewer.Models.Item("", i, "", "");

                for (var j = 0; j < row.length; j++) {
                    var f = new PivotViewer.Models.Facet(column[j]);
                    f.AddFacetValue(row[j]);
                    item.Facets.push(f);
                }

                collection.Items.push(item);
            }

            $.publish("/PivotViewer/Models/Collection/Loaded", null);
        };
    }
});
