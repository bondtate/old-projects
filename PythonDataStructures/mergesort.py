"""
PROJECT 3 - Merge Sort
Name: Tate Bond
PID: A550532302
"""

import copy
from Project3.LinkedList import LinkedList


def merge_lists(lists, threshold):
    '''
    - loop through the given list and call merge sort
      to sort the list
    - than merge the list with the linked list to be returned
    :param lists: a list of linked lists
    :param threshold: size of linked list to start insertion sort
    :return: the merged linked list
    '''
    r_list = LinkedList()

    for list in lists:
        list = merge_sort(list, threshold)
        r_list = merge(r_list, list)

    return r_list

def merge_sort(linked_list, threshold):
    '''
    -recursively break down the list until threshold is reached
    - then build back up using merge function
    :param linked_list: list to be sorted
    :param threshold: size of the linked list to start insertion sort
    :return: sorted linked list
    '''


    if len(linked_list) < 2:
        return linked_list

    split_lists = split_linked_list(linked_list)

    #if the list is greater than threshold continue merge else insertion sort
    if split_lists[0].length() > threshold:
        sorted1 = merge_sort(split_lists[0], threshold)
    else:
        split_lists[0].insertion_sort()
        sorted1 = split_lists[0]

    # if the list is greater than threshold continue merge else insertion sort
    if split_lists[1].length() > threshold:
        sorted2 = merge_sort(split_lists[1], threshold)
    else:
        split_lists[1].insertion_sort()
        sorted2 = split_lists[1]

    linked_list = merge(sorted1, sorted2)
    return linked_list


def split_linked_list(linked_list):
    '''
    -split the linked list in half
    -create two new lists with the halves
    :param linked_list: a single linked list
    :return: tuple containing 2 linked lists
    '''
    length = len(linked_list)
    llist1 = LinkedList()
    llist2 = LinkedList()

    #create a shallow copy of the linked_list
    temp_list = copy.copy(linked_list)

    #add the first half of the list
    for node in range(length//2):
        llist1.push_back(temp_list.pop_front())

    #add the second half of the list
    for node in range(length//2, len(linked_list)):
        llist2.push_back(temp_list.pop_front())

    r_val = (llist1, llist2)
    return r_val

def merge(list1, list2):
    '''
    -merge the two given lists back together
    -sorted in ascending order
    :param list1: linked list
    :param list2: linked list
    :return: one sorted linked list
    '''
    r_list = LinkedList()

    #loop until both lists are empty adding to r_list in ascending order
    while list1.is_empty() is False or list2.is_empty() is False:

        if list1.front_value() is None:
            r_list.push_back(list2.pop_front())

        elif list2.front_value() is None:
            r_list.push_back(list1.pop_front())

        elif list2.front_value() <= list1.front_value():
            r_list.push_back(list2.pop_front())

        else:
            r_list.push_back(list1.pop_front())

    return r_list

#def main():
    #pass
    #l = []
    #for i in range(1):
        #num = random.randint(1, 20)
        #l.append(num)




    # --------------------------------------


    #llist = LinkedList(l)
    #llist.insertion_sort()
    #print(llist)




    #blist.insertion_sort()
    #print(blist)

    #blist = merge(llist, blist)
    #print(blist)

    #llist = merge_sort(llist, 0)


#if __name__ == '__main__':
#    main()