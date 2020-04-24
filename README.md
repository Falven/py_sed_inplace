# py_sed_inplace

Edit a file in-place using a powerful Python Regular Expression!

>Authoring a homegrown sed replacement in pure Python with no external commands or additional dependencies is a noble task laden with noble landmines. Who would have thought?
>Nonetheless, it is feasible. It's also desirable. We've all been there, people: "I need to munge some plaintext files, but I only have Python, two plastic shoelaces, and a moldy can of bunker-grade Maraschino cherries. Help."

Credit to *Cecil Curry* on StackOverflow. Thanks for your whimsical humour.

## Usage

```
sed_inplace.py -p <pattern> -r <replacement> -f <file>
sed_inplace.py --patern <pattern> --replacement <replacement> --file <file>
```

### Pattern

The pattern must be a Python-compatible Regular Expression. Test it over at [regex101.com](https://regex101.com/r/QfFaCY/10).

Ensure that the regular expression is properly escaped for your shell of choice, or use a string literal to avoid having to escape at all!

### Flags

Python allows pattern flags to be passed in as the **first item** in the regular expression in the format:
`(?aiLmsux-imsx:...)` where `'a', 'i', 'L', 'm', 's', 'u', 'x'` correspond with their respective regex flags.
See [the documentation](https://docs.python.org/3/library/re.html#re.Pattern.flags) for more information.

### Replacement

From [the python documentation](https://docs.python.org/3/library/re.html#re.sub):

>In string-type repl arguments, in addition to the character escapes and backreferences described above, \g<name> will use the substring matched by the group named name, as defined by the (?P<name>...) syntax. \g<number> uses the corresponding group number; \g<2> is therefore equivalent to \2, but isn’t ambiguous in a replacement such as \g<2>0. \20 would be interpreted as a reference to group 20, not a reference to group 2 followed by the literal character '0'. The backreference \g<0> substitutes in the entire substring matched by the RE.

### File

The path to the file to edit in-place. The script will create a temporary copy of the file to perform the replacement, and then overwrite the file with the replacement.

## Examples

Powershell Core:
```powershell
python ./sed_inplace.py -p '(?ims)^(<Directory\s*\"\/var\/www\/html\">.*?AllowOverride\s*)(None|All|Options|FileInfo|AuthConfig|Limit)+(.*?<\/Directory>)$' -r '\g<1>All\g<3>' -i './tests/httpd.conf'
```

Will find the `AllowOverride None` item in the `<Directory "/var/www/html">` section of the provided default Apache config file `httpd.conf` in the tests project directory, and replace it with `AllowOverride All`.

Before sed_inplace command:
```xml
<Directory "/var/www/html">
    #
    # Possible values for the Options directive are "None", "All",
    # or any combination of:
    #   Indexes Includes FollowSymLinks SymLinksifOwnerMatch ExecCGI MultiViews
    #
    # Note that "MultiViews" must be named *explicitly* --- "Options All"
    # doesn't give it to you.
    #
    # The Options directive is both complicated and important.  Please see
    # http://httpd.apache.org/docs/2.4/mod/core.html#options
    # for more information.
    #
    Options Indexes FollowSymLinks

    #
    # AllowOverride controls what directives may be placed in .htaccess files.
    # It can be "All", "None", or any combination of the keywords:
    #   Options FileInfo AuthConfig Limit
    #
    AllowOverride None

    #
    # Controls who can get stuff from this server.
    #
    Require all granted
</Directory>
```

After sed_inplace command:
```xml
<Directory "/var/www/html">
    #
    # Possible values for the Options directive are "None", "All",
    # or any combination of:
    #   Indexes Includes FollowSymLinks SymLinksifOwnerMatch ExecCGI MultiViews
    #
    # Note that "MultiViews" must be named *explicitly* --- "Options All"
    # doesn't give it to you.
    #
    # The Options directive is both complicated and important.  Please see
    # http://httpd.apache.org/docs/2.4/mod/core.html#options
    # for more information.
    #
    Options Indexes FollowSymLinks

    #
    # AllowOverride controls what directives may be placed in .htaccess files.
    # It can be "All", "None", or any combination of the keywords:
    #   Options FileInfo AuthConfig Limit
    #
    AllowOverride All

    #
    # Controls who can get stuff from this server.
    #
    Require all granted
</Directory>
```
