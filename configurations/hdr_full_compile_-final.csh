# HDR Full Compile -final (slow!)
rm {path}/{file}.bsp
rm {bspdir}/{file}.bsp
{bsp} -game {gamedir} {path}/{file}
{vis} -game {gamedir} {path}/{file}
{rad} -both -final -game {gamedir} {path}/{file}
cp {path}/{file}.bsp {bspdir}/{file}.bsp
{game} -dev -console -allowdebug -game {gamedir} +map {file}
