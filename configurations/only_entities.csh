# Only Entities
{bsp} -onlyents -game {gamedir} {path}/{file}
{vis} -game {gamedir} {path}/{file}
{rad} -both -final -game {gamedir} {path}/{file}
cp {path}/{file}.bsp {bspdir}/{file}.bsp
{game} -allowdebug -game {gamedir} +map {file}
