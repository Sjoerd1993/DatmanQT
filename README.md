This program is free software.
It is licensed under the GNU GPL version 3 or later.
That means you are free to use this program for any purpose;
free to study and modify this program to suit your needs;
and free to share this program or your modifications with anyone.
If you share this program or your modifications
you must grant the recipients the same freedoms.
To be more specific: you must share the source code under the same license.
For details see https://www.gnu.org/licenses/gpl-3.0.html

# Datman
Data manipulator, will mainly be useful for plotting graphs and doing basic manipulation on them such as cutting, translations and multiplications.

Early beta version. The following features are implemented at the moment:
- Opening and plotting an arbitrary amount of two-column text files with XY-data
- Selection of this data
- Cutting selected data from graph
- Normalization of data
- Translation of data
- Multiplication of data
- Center highest Y-value of data at x = 0
- Smoothening of data (both at linear and log scale)
- Saving new edited data as txt file

Other convenient features are implemented as well such as change of both x- and y scale, editing of above operations on either all imported data
on one of the selected data files. Selected data is highlighted as well, and the selection tool uses a convenient draggable ROI.

Planned features include an undo functionality, and perhaps a port away from Qt to GTK.