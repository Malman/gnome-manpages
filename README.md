# gnome-manpages

This repository contains section 3 manpages for various gnome related libraries.
These were generated from in-tree gtk-doc style documentation generated with --enable-gtk-doc for each of the projects.
The .xml files were processed using xsltproc to convert from docbook to manpage.
Then the .xml files were processed for refentry2 links to build the function, macro, type, and struct links.

To install.

```sh
sudo ./install.sh
```

Now you will be able to search for for things like:

```sh
man -k g_ptr_ar
g_ptr_array_add (3)  - arrays of pointers to any type of data, which grow automatically as new elements are added
g_ptr_array_foreach (3) - arrays of pointers to any type of data, which grow automatically as new elements are added
g_ptr_array_free (3) - arrays of pointers to any type of data, which grow automatically as new elements are added
g_ptr_array_index (3) - arrays of pointers to any type of data, which grow automatically as new elements are added
g_ptr_array_new (3)  - arrays of pointers to any type of data, which grow automatically as new elements are added
g_ptr_array_new_full (3) - arrays of pointers to any type of data, which grow automatically as new elements are added
g_ptr_array_new_with_free_func (3) - arrays of pointers to any type of data, which grow automatically as new elements are added
g_ptr_array_ref (3)  - arrays of pointers to any type of data, which grow automatically as new elements are added
g_ptr_array_remove (3) - arrays of pointers to any type of data, which grow automatically as new elements are added
g_ptr_array_remove_fast (3) - arrays of pointers to any type of data, which grow automatically as new elements are added
g_ptr_array_remove_index (3) - arrays of pointers to any type of data, which grow automatically as new elements are added
g_ptr_array_remove_index_fast (3) - arrays of pointers to any type of data, which grow automatically as new elements are added
g_ptr_array_remove_range (3) - arrays of pointers to any type of data, which grow automatically as new elements are added
g_ptr_array_set_free_func (3) - arrays of pointers to any type of data, which grow automatically as new elements are added
g_ptr_array_set_size (3) - arrays of pointers to any type of data, which grow automatically as new elements are added
g_ptr_array_sized_new (3) - arrays of pointers to any type of data, which grow automatically as new elements are added
g_ptr_array_sort (3) - arrays of pointers to any type of data, which grow automatically as new elements are added
g_ptr_array_sort_with_data (3) - arrays of pointers to any type of data, which grow automatically as new elements are added
g_ptr_array_unref (3) - arrays of pointers to any type of data, which grow automatically as new elements are added
```

Also, Shift+K should work in VIM to see the documentation on the type, macro, or function.

# Building manpages for your project

Make sure you configure your project with --enable-gtk-doc to generate your
reference documentation. Then run the gtkdoc2man.py script provided in this
repository.

```sh
cd doc/reference/my
/path/to/gtkdoc2man.py -o man/ --prefix=My '--book=My Reference' --section=3 my-docs.sgml
```

In the example above, the man pages will be placed in the directory man/.
