create database agenda;
use agenda;
create table persona(
ID_persona int primary  key auto_increment,
 P_Nombre varchar (45) not null, 
 p_Apellido varchar (45) not null,  
 p_Email varchar (45) not null,  
 p_Direccion varchar (45) not null, 
 p_Telefono int not null, 
 p_Usuario varchar (45) not null, 
 p_Contraseña varchar (255) not null,
 Roles varchar(55) not null
);

create table canciones(
ID_Cancion int primary  key auto_increment,
 Titulo varchar (60) not null, 
 Artista varchar (60) not null,  
 Genero varchar (60) not null,  
 Precio decimal (10,0) not null, 
 Duracion varchar (10) not null, 
 A_Lanzamiento date  not null, 
 img blob not null
);

create table compras(
ID_Compra int primary  key auto_increment,
 Fecha_Compra date not null, 
 Precio decimal (10,0) not null, 
 ID_persona int not null,
 ID_Cancion int not null,
 MPago varchar(50) not null,
 foreign key (ID_persona) references persona(ID_persona),
 foreign key (ID_Cancion) references canciones(ID_Cancion)
);
