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
        function getFilterData(){
            var data = {}
            $('#objectFilterForm input').each(function(index, value) {
              var key = $(value).attr('name');
              var val = $(value).val();
              data[key] = val
            });
            return data      
        }

        function fetchData(){
          var searchParams = new URLSearchParams(window.location.search)
          var url = $('#objectFilterForm').data('url');
          var data = getFilterData();
            for(var key in data){
              searchParams.append(key,data[key]);
            }
          $('#tableData').load(url + " #objTable", searchParams.toString());
        }