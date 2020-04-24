# py_sed_inplace
Sed implementation using python Regular Expressions

Edit a file in-place using a powerful Python regular expression.

>Authoring a homegrown sed replacement in pure Python with no external commands or additional dependencies is a noble task laden with noble landmines. Who would have thought?
>Nonetheless, it is feasible. It's also desirable. We've all been there, people: "I need to munge some plaintext files, but I only have Python, two plastic shoelaces, and a moldy can of bunker-grade Maraschino cherries. Help."

Credit to *Cecil Curry* on StackOverflow. Thanks for your whimsical humour.

## Usage

```
sed_inplace.py -p <pattern> -r <replacement> -f <file>
sed_inplace.py --patern <pattern> --replacement <replacement> --file <file>
```
  
The pattern must be a Python-compatible Regular Expression. Test it over at [regex101.com](https://regex101.com/r/QfFaCY/10).

Ensure that the regular expression is properly escaped for your shell of choice, or use a string literal to avoid having to escape at all!

### Flags

Python allows pattern flags to be passed in as the **first item** in the regular expression in the format:
`(?aiLmsux-imsx:...)` where 'a', 'i', 'L', 'm', 's', 'u', 'x' correspond with their respective regex flags.
See [the documentation](https://docs.python.org/3/library/re.html#re.Pattern.flags) for more information.

### Examples

Powershell Core:
```powershell
python ./sed_inplace.py -p '(?ims)^(<Directory\s*\"\/var\/www\/html\">.*?AllowOverride\s*)(None|All|Options|FileInfo|AuthConfig|Limit)+(.*?<\/Directory>)$' -r '\g<1>All\g<3>' -i 'httpd.conf'
```
