        // Function for sorting products (ascending or descending)
        function sort(tag){
            var ordering = $(tag).data('ordering');
            var searchParams = new URLSearchParams(window.location.search)
            var url = $(tag).data('url');
            searchParams.append("ordering",ordering);
            var data = getFilterData();
            for(var key in data){
              searchParams.append(key,data[key]);
            }
            $('#tableData').load(url + " #objTable", searchParams.toString());

        }
        // Function for moving columns to left or right
        function moveColumn(tag){
            var column = $(tag).data('column');
            console.log(column)
            var direction = $(tag).data('move');
            console.log(direction)
            var url = $(tag).data('url');
            var searchParams = new URLSearchParams(window.location.search)
            searchParams.append("column",column);
            searchParams.append("direction", direction);
            var data = getFilterData();
            for(var key in data){
              searchParams.append(key,data[key]);
            }
            $('#tableData').load(url + " #objTable", searchParams.toString());
        }
        $('#objectFilterForm').find('input').addClass('form-control')

        // Get filter data
        function getFilterData(filterId){
            var data = {}
            // Get values from the filter text inputs
            var tags = "#"+filterId + ' input';
            console.log(tags);
            $(tags).each(function(index, tag) {
              var key = $(tag).attr('name');
              var val = $(tag).val();
              data[key] = val
            });
            // Get values to exclude (we need to exclude objects which are selected in the selection pane 
            // and filter them out in the back end from the queryset so they are not see in the proposed list)
            var exclude_ids = []
            $('#selection_pane_table tbody tr').each(function(ind, tag){
              exclude_ids.push($(tag).data('id'));
            })
            data['exclude'] = exclude_ids;
            console.log(data)
            return data      
        }
        
        //This function fetches object list as an HTML response. It then replaces the innerHTML of the 
        // outerDiv with the innerDiv (not its contents) of the HTML response.
        // function fetchData(){
        //   var searchParams = new URLSearchParams(window.location.search)
        //   var url = $('#'+filterForm).data('url');
        //   var data = getFilterData(filterForm);
        //     for(var key in data){
        //       searchParams.append(key,data[key]);
        //     }
        //     searchParams.append('form', filterForm); // Used to identify which table is calling (object or selection)
        //     // Here objTable (innerDiv) element received from the display view will be the same despite of the type of table 
        //     // that requests the data.
        //     $('#'+outerDiv).load(url + " #"+innerDiv, searchParams.toString());
            
        // }

        function fetchData(element){
          var searchParams = new URLSearchParams(window.location.search)
          var filterId = $(element).parent().parent().attr('id')
          var url = $(element).parent().parent().data('url');
          var data = getFilterData(filterId);
            for(var key in data){
              searchParams.append(key,data[key]);
            }
            searchParams.append('form', filterId); // Used to identify which table is calling (object or selection)
            // Here objTable (innerDiv) element received from the display view will be the same despite of the type of table 
            // that requests the data.
            if(filterId=='objectFilterForm'){
              $('#tableData').load(url + " #objTable", searchParams.toString(),function(){enableHighlight()});
            }
            else if(filterId == 'selectionFilterForm'){
              $('#selectionTableOuterDiv').load(url + " #selectionTableInnerDiv", searchParams.toString(), function(){enableHighlight()});
            }        
          }

          function updateTable(table_type){ // table --> display or selection
            console.log('I am in updateTable!')
            if(table_type == 'display'){
              var filterId = 'objectFilterForm';
              var url = $('#objectFilterForm').data('url');
            }
            else if(table_type == 'selection'){
              var filterId = 'selectionFilterForm';
              var url = $('#selectionFilterForm').data('url');
            }
            console.log(filterId,url)
            var searchParams = new URLSearchParams(window.location.search)
            var data = getFilterData(filterId);
              for(var key in data){
                searchParams.append(key,data[key]);
              }
              searchParams.append('form', filterId); // Used to identify which table is calling (object or selection)
              // Here objTable (innerDiv) element received from the display view will be the same despite of the type of table 
              // that requests the data.
              if(filterId=='objectFilterForm'){
                $('#tableData').load(url + " #objTable", searchParams.toString(),function(){enableHighlight()});
              }
              else if(filterId == 'selectionFilterForm'){
                $('#selectionTableOuterDiv').load(url + " #selectionTableInnerDiv", searchParams.toString(), function(){enableHighlight()});
              }        
            }