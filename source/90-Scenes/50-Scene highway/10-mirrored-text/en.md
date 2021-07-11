# The text written on my vehicles is (sometimes) flipped!

{=macro(zoomable-image-left, Truck coloring page with text, images/scene-highway-writing-mirrored-truck-drawing.jpg)}
On the {=property(scene-translated)} coloring pages, the vehicles are drawn as going from right to left.
{: class=clearfix}

{=macro(zoomable-image-left, Screenshot of truck with text going from right to left, images/scene-highway-writing-mirrored-truck-right-to-left.jpg)}
That's fine, if they really go from right to left on the screen.
{: class=clearfix}

{=macro(zoomable-image-left, Screenshot of truck with text going from left to right, images/scene-highway-writing-mirrored-truck-left-to-right.jpg)}
But on the opposing lane, they of course have to go from left to right.
So the vehicles need to get mirrored.

If they have some text written on them, this text of course gets mirrored along as well and appears flipped, if the vehicle is going from left to right.
{: class=clearfix}

Vehicles that come with text already on their coloring page are the exception (e.g., the "POLICE" mark on the police car).
There, Scanarium knows where the text is can exclude that part when mirroring the vehicle.
So the text is readable regardless of the direction the vehicle is going in:

{=macro(zoomable-image-left, Screenshot of police car going from right to left, images/scene-highway-writing-mirrored-police-car-right-to-left.jpg)}
{=macro(zoomable-image-left, Screenshot of police car going from left to right, images/scene-highway-writing-mirrored-police-car-left-to-right.jpg)}
{: class=clearfix}

version: 1.000
