
from django.core.paginator import Paginator


def get_columns(state):
    """Gets the columns of the display table.
    
    This function takes a filter state and returns an array of column names that are
    ordered depending on the position attribute of the columns. This order is important 
    as the queryset will be rendered in the display table according to the column order
    in this returned array.
    
    Parameters
    ----------
    state : FilterState
        Filter state of the columns.
        
    Returns
    -------
    List
        A list that dictates the order of the columns.

    """
    a=[]
    b=[]
    c=[]
    cols = state.filtercolumn_set.all()
    for col in cols:
        if col.visible == True:
            b.append(col.position)
            c.append(col.name)
    for i in range(0,len(b)):
        k = -1
        index = 0
        for j,val in enumerate(b):
            if val>k:
                k=val
                index = j
        a.append(c.pop(index))
        b.pop(index)
        a=a[::-1] # reverses the array

    return a


def sort_ascending_descending(request,model):
    """Sorts and saves the state of the column.
    
    This function takes a request, finds which column needs to be sorted in ascending/descending
    order, and returns the sorted queryset.
    
    Parameters
    ----------
    request : HttpRequest
        ``GET`` request received for retreiving the list of model instances.
    model : Model
        Model of the objects being retrieved.
    
    Returns
    -------
    QuerySet 
        List of sorted object instances.
    """
    try:
        if request.GET.get('sort')=='ascend': 
            queryset = model.objects.all().order_by(request.GET.get('column'))
        else:
            queryset = model.objects.all().order_by("-"+request.GET.get('column'))
    except TypeError:
        queryset = model.objects.all()

    return queryset


def change_column_position(request,state):
    """Modifies the column states depending on the request.
    
    This function:
        - Takes a filter state
        - Extracts the column names into an order array
        - Modifies the column order in the array depending on user input direction (left/right)
        - Saves this modified state of columns into the database
        - Returns the modified column names array
        
    Parameters
    ----------
    request : HttpRequest
        ``GET`` request for retrieving the state of the columns.
    state : FilterState
        Filter state of the columns.
    
    Returns
    -------
    List
        List of sorted columns.
    """

    def modify_column_list(request,column_list):
        col = request.GET.get('column')
        print(col)
        old_index = column_list.index(col)
        if request.GET.get('direction')=='left':
            if old_index == 0:
                new_index = old_index
            else:
                new_index = old_index - 1
        else:
            if old_index == len(column_list)-1:
                new_index = old_index
            else:
                new_index = old_index + 1
        column_list.insert(new_index, column_list.pop(old_index))       
        return column_list, old_index, new_index    

    def save_column_change_to_database(state, column_list, old_index, new_index):
        master_col_name = column_list[new_index]
        slave_col_name = column_list[old_index]
        master_col = state.filtercolumn_set.get(name=master_col_name)
        slave_col = state.filtercolumn_set.get(name=slave_col_name)
        temp_pos = master_col.position
        master_col.position = slave_col.position
        master_col.save()
        slave_col.position = temp_pos
        slave_col.save()
        return
        
    column_list = get_columns(state) # get initial list of columns
    try:
        if request.GET.get('direction') != None and request.GET.get('column') != None:
            column_list, old_index, new_index =  modify_column_list(request,column_list)
            save_column_change_to_database(state, column_list, old_index, new_index)
    except ValueError:
        pass

    return column_list


def paginate(queryset,filter,page_number):
    """Paginates the list of objects.
    
    This function takes the entire queryset and filters out only objects belonging to the
    request page
    
    Parameters
    ----------
    queryset : QuerySet
        ``QuerySet`` of the objects retrieved from the database.
    filter : FilterState
        Filter state of the columns.
    page_number : int
        Page number requested.
    """
    paginator = Paginator(queryset,15)
    page_obj = paginator.get_page(page_number)
    page_obj_dicts = []
    for prod in page_obj: 
        page_obj_dicts.append(prod.__dict__)
    return page_obj, page_obj_dicts