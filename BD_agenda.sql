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
 p_Contraseña varchar (45) not null
);