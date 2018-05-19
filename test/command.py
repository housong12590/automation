from docker.cli.automation import get_image_name

# print(get_image_name())
import re

result = '0b87b5a16fab61522d833ce6924d063eebc1c8861130c7254a61a3ccacd59424'
r = re.match(r'\w+', result)
if  r:
    print(r)
