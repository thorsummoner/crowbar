# HDR Full Compile
rm {path}/{file}.bsp
rm {bspdir}/{file}.bsp
{bsp} -game {gamedir} {path}/{file}
{vis} -game {gamedir} {path}/{file}
{rad} -both -game {gamedir} {path}/{file}
cp {path}/{file}.bsp {bspdir}/{file}.bsp
{game} -dev -console -allowdebug -game {gamedir} +map {file}
