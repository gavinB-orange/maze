maze
====

Just for fun ...

TODO:

* Currently not all the fill in paths do link to existing corridors - the problem is that the I do not inc the
  path_count for the fill_in walks, and this means that I can get blocked by fill_in walks.
  Possibly I should increment the path_count for fill_in as well, but that needs to be done carefully as I'm not
  sure that it won't break the starting_pos routine.

* I am getting "thick" corridors as I am treating walls differently for fill_in and non fill_in.
