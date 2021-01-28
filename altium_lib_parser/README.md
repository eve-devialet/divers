# Parsing Altium lib

The tip is to export a schematic lib in .lia format, corresponding to a P-CAD library, which has the good taste to be a text format. Then it is possible to re-import a modified .lia using the Import Wizard.

Be careful, Altium is very sensitive to encoding and line feeds: modified file must be \\r\\n line breaks and ISO-8859-1 encoding.

## Post-treatment
Some data is lost during the import/export process.

* Use the SCHLIB List panel to display all parameters, and set them all to the right color and font.
* Use SHIFT-F to select all "PartNumber" parameters, modify the display boolean, color, font and position
Alternativery, use SCHLIB Filter panel and request: "(ObjectKind = 'Parameter') And (ParameterName = 'PartNumber')"
* Also use SHIFT-F to select all designators, change them to R? instead of U?, and modify display options
SCHLIB Filter request: "ObjectKind = 'Designator'"
* Select all parameters and toggle PartNumber and Designator visibility.
SCHLIB Filter request: "ObjectKind = 'Part'"

### To be fixed
* Description fields are empty
* Bug with designator display
