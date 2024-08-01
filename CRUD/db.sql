USE [master]
GO
/****** Object:  Database [TerraForce]    Script Date: 8/1/2024 7:55:45 AM ******/
CREATE DATABASE [TerraForce]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'TerraForce', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\DATA\TerraForce.mdf' , SIZE = 8192KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON 
( NAME = N'TerraForce_log', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\DATA\TerraForce_log.ldf' , SIZE = 8192KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
 WITH CATALOG_COLLATION = DATABASE_DEFAULT, LEDGER = OFF
GO
ALTER DATABASE [TerraForce] SET COMPATIBILITY_LEVEL = 160
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [TerraForce].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [TerraForce] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [TerraForce] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [TerraForce] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [TerraForce] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [TerraForce] SET ARITHABORT OFF 
GO
ALTER DATABASE [TerraForce] SET AUTO_CLOSE OFF 
GO
ALTER DATABASE [TerraForce] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [TerraForce] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [TerraForce] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [TerraForce] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [TerraForce] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [TerraForce] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [TerraForce] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [TerraForce] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [TerraForce] SET  ENABLE_BROKER 
GO
ALTER DATABASE [TerraForce] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [TerraForce] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [TerraForce] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [TerraForce] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [TerraForce] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [TerraForce] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [TerraForce] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [TerraForce] SET RECOVERY FULL 
GO
ALTER DATABASE [TerraForce] SET  MULTI_USER 
GO
ALTER DATABASE [TerraForce] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [TerraForce] SET DB_CHAINING OFF 
GO
ALTER DATABASE [TerraForce] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [TerraForce] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO
ALTER DATABASE [TerraForce] SET DELAYED_DURABILITY = DISABLED 
GO
ALTER DATABASE [TerraForce] SET ACCELERATED_DATABASE_RECOVERY = OFF  
GO
EXEC sys.sp_db_vardecimal_storage_format N'TerraForce', N'ON'
GO
ALTER DATABASE [TerraForce] SET QUERY_STORE = ON
GO
ALTER DATABASE [TerraForce] SET QUERY_STORE (OPERATION_MODE = READ_WRITE, CLEANUP_POLICY = (STALE_QUERY_THRESHOLD_DAYS = 30), DATA_FLUSH_INTERVAL_SECONDS = 900, INTERVAL_LENGTH_MINUTES = 60, MAX_STORAGE_SIZE_MB = 1000, QUERY_CAPTURE_MODE = AUTO, SIZE_BASED_CLEANUP_MODE = AUTO, MAX_PLANS_PER_QUERY = 200, WAIT_STATS_CAPTURE_MODE = ON)
GO
USE [TerraForce]
GO
/****** Object:  Table [dbo].[Asociacion]    Script Date: 8/1/2024 7:55:45 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Asociacion](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[id_escuela] [int] NULL,
	[id_empresa] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Calles]    Script Date: 8/1/2024 7:55:45 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Calles](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[nombre] [varchar](150) NULL,
	[id_colonia] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Colonias]    Script Date: 8/1/2024 7:55:45 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Colonias](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[nombre] [varchar](150) NULL,
	[id_municipio] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Convocatorias]    Script Date: 8/1/2024 7:55:45 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Convocatorias](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[titulo] [varchar](100) NULL,
	[descripcion] [varchar](1000) NULL,
	[requisitos] [varchar](500) NULL,
	[fecha_inicio] [date] NULL,
	[usuarios_registrados] [int] NULL,
	[id_estatus] [int] NULL,
	[id_empresa] [int] NULL,
	[id_tematica] [int] NULL,
	[imagen] [varbinary](max) NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[ConvocatoriasEstatus]    Script Date: 8/1/2024 7:55:45 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[ConvocatoriasEstatus](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[estatus] [varchar](150) NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Direcciones]    Script Date: 8/1/2024 7:55:45 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Direcciones](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[id_estado] [int] NULL,
	[id_municipio] [int] NULL,
	[id_colonia] [int] NULL,
	[id_calle] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Empresas]    Script Date: 8/1/2024 7:55:45 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Empresas](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[nombre] [varchar](150) NULL,
	[id_correo] [int] NULL,
	[id_telefono] [int] NULL,
	[id_direccion] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Escuelas]    Script Date: 8/1/2024 7:55:45 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Escuelas](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[nombre] [varchar](150) NULL,
	[id_direccion] [int] NULL,
	[id_telefonos] [int] NULL,
	[id_correos] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Estados]    Script Date: 8/1/2024 7:55:45 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Estados](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[nombre] [varchar](150) NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Municipios]    Script Date: 8/1/2024 7:55:45 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Municipios](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[nombre] [varchar](150) NULL,
	[id_estado] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Personas]    Script Date: 8/1/2024 7:55:45 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Personas](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[nombre] [varchar](150) NULL,
	[apellidop] [varchar](150) NULL,
	[apellidom] [varchar](150) NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Registros]    Script Date: 8/1/2024 7:55:45 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Registros](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[id_voluntario] [int] NULL,
	[id_convocatoria] [int] NULL,
	[fecha] [date] NULL,
	[hora] [time](7) NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Telefonos]    Script Date: 8/1/2024 7:55:45 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Telefonos](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[telefono] [varchar](150) NULL,
	[id_tipo] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Tematicas]    Script Date: 8/1/2024 7:55:45 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Tematicas](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[tematica] [varchar](150) NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[TiposUsuarios]    Script Date: 8/1/2024 7:55:45 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[TiposUsuarios](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[tipo] [varchar](150) NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[TipoTelefonos]    Script Date: 8/1/2024 7:55:45 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[TipoTelefonos](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[tipo] [varchar](150) NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Usuarios]    Script Date: 8/1/2024 7:55:45 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Usuarios](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[id_persona] [int] NULL,
	[id_tipouser] [int] NULL,
	[correo] [varchar](150) NULL,
	[passwrd] [varchar](25) NULL,
	[id_empresa] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Voluntarios]    Script Date: 8/1/2024 7:55:45 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Voluntarios](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[id_escuela] [int] NULL,
	[id_persona] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
SET IDENTITY_INSERT [dbo].[Asociacion] ON 

INSERT [dbo].[Asociacion] ([id], [id_escuela], [id_empresa]) VALUES (3, 3, 3)
SET IDENTITY_INSERT [dbo].[Asociacion] OFF
GO
SET IDENTITY_INSERT [dbo].[Calles] ON 

INSERT [dbo].[Calles] ([id], [nombre], [id_colonia]) VALUES (1, N'Avenida Paulista', 1)
INSERT [dbo].[Calles] ([id], [nombre], [id_colonia]) VALUES (2, N'Avenida Atlântica', 2)
INSERT [dbo].[Calles] ([id], [nombre], [id_colonia]) VALUES (3, N'Avenida Cristóvão Colombo', 3)
SET IDENTITY_INSERT [dbo].[Calles] OFF
GO
SET IDENTITY_INSERT [dbo].[Colonias] ON 

INSERT [dbo].[Colonias] ([id], [nombre], [id_municipio]) VALUES (1, N'Jardim Paulista', 1)
INSERT [dbo].[Colonias] ([id], [nombre], [id_municipio]) VALUES (2, N'Copacabana', 2)
INSERT [dbo].[Colonias] ([id], [nombre], [id_municipio]) VALUES (3, N'Savassi', 3)
SET IDENTITY_INSERT [dbo].[Colonias] OFF
GO
SET IDENTITY_INSERT [dbo].[Convocatorias] ON 

INSERT [dbo].[Convocatorias] ([id], [titulo], [descripcion], [requisitos], [fecha_inicio], [usuarios_registrados], [id_estatus], [id_empresa], [id_tematica], [imagen]) VALUES (1, N'Convocatoria São Paulo', N'Descripción São Paulo', N'Requisitos São Paulo', CAST(N'2024-07-01' AS Date), 10, 1, 1, 1, NULL)
INSERT [dbo].[Convocatorias] ([id], [titulo], [descripcion], [requisitos], [fecha_inicio], [usuarios_registrados], [id_estatus], [id_empresa], [id_tematica], [imagen]) VALUES (2, N'Convocatoria Rio', N'Descripción Rio', N'Requisitos Rio', CAST(N'2024-07-02' AS Date), 20, 2, 2, 2, NULL)
INSERT [dbo].[Convocatorias] ([id], [titulo], [descripcion], [requisitos], [fecha_inicio], [usuarios_registrados], [id_estatus], [id_empresa], [id_tematica], [imagen]) VALUES (3, N'Convocatoria Minas', N'Descripción Minas', N'Requisitos Minas', CAST(N'2024-07-03' AS Date), 30, 1, 3, 1, NULL)
SET IDENTITY_INSERT [dbo].[Convocatorias] OFF
GO
SET IDENTITY_INSERT [dbo].[ConvocatoriasEstatus] ON 

INSERT [dbo].[ConvocatoriasEstatus] ([id], [estatus]) VALUES (1, N'Abierta')
INSERT [dbo].[ConvocatoriasEstatus] ([id], [estatus]) VALUES (2, N'Cerrada')
SET IDENTITY_INSERT [dbo].[ConvocatoriasEstatus] OFF
GO
SET IDENTITY_INSERT [dbo].[Direcciones] ON 

INSERT [dbo].[Direcciones] ([id], [id_estado], [id_municipio], [id_colonia], [id_calle]) VALUES (1, 1, 1, 1, 1)
INSERT [dbo].[Direcciones] ([id], [id_estado], [id_municipio], [id_colonia], [id_calle]) VALUES (2, 2, 2, 2, 2)
INSERT [dbo].[Direcciones] ([id], [id_estado], [id_municipio], [id_colonia], [id_calle]) VALUES (3, 3, 3, 3, 3)
SET IDENTITY_INSERT [dbo].[Direcciones] OFF
GO
SET IDENTITY_INSERT [dbo].[Empresas] ON 

INSERT [dbo].[Empresas] ([id], [nombre], [id_correo], [id_telefono], [id_direccion]) VALUES (1, N'Empresa de Deportes São Paulo', 1, 1, 1)
INSERT [dbo].[Empresas] ([id], [nombre], [id_correo], [id_telefono], [id_direccion]) VALUES (2, N'Empresa de Deportes Rio', 2, 2, 2)
INSERT [dbo].[Empresas] ([id], [nombre], [id_correo], [id_telefono], [id_direccion]) VALUES (3, N'Empresa de Deportes Minas', 3, 1, 3)
SET IDENTITY_INSERT [dbo].[Empresas] OFF
GO
SET IDENTITY_INSERT [dbo].[Escuelas] ON 

INSERT [dbo].[Escuelas] ([id], [nombre], [id_direccion], [id_telefonos], [id_correos]) VALUES (1, N'Escuela de Fútbol São Paulo', 1, 1, 1)
INSERT [dbo].[Escuelas] ([id], [nombre], [id_direccion], [id_telefonos], [id_correos]) VALUES (2, N'Escuela de Fútbol Rio', 2, 2, 2)
INSERT [dbo].[Escuelas] ([id], [nombre], [id_direccion], [id_telefonos], [id_correos]) VALUES (3, N'Escuela de Fútbol Minas', 3, 1, 3)
SET IDENTITY_INSERT [dbo].[Escuelas] OFF
GO
SET IDENTITY_INSERT [dbo].[Estados] ON 

INSERT [dbo].[Estados] ([id], [nombre]) VALUES (1, N'São Paulo')
INSERT [dbo].[Estados] ([id], [nombre]) VALUES (2, N'Rio de Janeiro')
INSERT [dbo].[Estados] ([id], [nombre]) VALUES (3, N'Minas Gerais')
SET IDENTITY_INSERT [dbo].[Estados] OFF
GO
SET IDENTITY_INSERT [dbo].[Municipios] ON 

INSERT [dbo].[Municipios] ([id], [nombre], [id_estado]) VALUES (1, N'São Paulo', 1)
INSERT [dbo].[Municipios] ([id], [nombre], [id_estado]) VALUES (2, N'Rio de Janeiro', 2)
INSERT [dbo].[Municipios] ([id], [nombre], [id_estado]) VALUES (3, N'Belo Horizonte', 3)
SET IDENTITY_INSERT [dbo].[Municipios] OFF
GO
SET IDENTITY_INSERT [dbo].[Personas] ON 

INSERT [dbo].[Personas] ([id], [nombre], [apellidop], [apellidom]) VALUES (1, N'Ronaldo', N'Augustus', N'Cicero')
INSERT [dbo].[Personas] ([id], [nombre], [apellidop], [apellidom]) VALUES (2, N'Ronaldinho', N'Tiberius', N'Seneca')
INSERT [dbo].[Personas] ([id], [nombre], [apellidop], [apellidom]) VALUES (3, N'Pelé', N'Nero', N'Claudius')
INSERT [dbo].[Personas] ([id], [nombre], [apellidop], [apellidom]) VALUES (4, N'Zico', N'Maximus', N'Julius')
INSERT [dbo].[Personas] ([id], [nombre], [apellidop], [apellidom]) VALUES (6, N'richy', N'sandoval', N'ayuda')
INSERT [dbo].[Personas] ([id], [nombre], [apellidop], [apellidom]) VALUES (7, N'Samuel', N'pana', N'dero')
INSERT [dbo].[Personas] ([id], [nombre], [apellidop], [apellidom]) VALUES (8, N'Salomon Pedro', N'Torres', N'Sanchez')
INSERT [dbo].[Personas] ([id], [nombre], [apellidop], [apellidom]) VALUES (9, N'Angela', N'aguilar', N'aquilar')
INSERT [dbo].[Personas] ([id], [nombre], [apellidop], [apellidom]) VALUES (10, N'Ismael ', N'Zambada', N'Guzman')
SET IDENTITY_INSERT [dbo].[Personas] OFF
GO
SET IDENTITY_INSERT [dbo].[Registros] ON 

INSERT [dbo].[Registros] ([id], [id_voluntario], [id_convocatoria], [fecha], [hora]) VALUES (1, 1, 1, CAST(N'2024-07-01' AS Date), CAST(N'10:00:00' AS Time))
INSERT [dbo].[Registros] ([id], [id_voluntario], [id_convocatoria], [fecha], [hora]) VALUES (2, 2, 2, CAST(N'2024-07-02' AS Date), CAST(N'11:00:00' AS Time))
SET IDENTITY_INSERT [dbo].[Registros] OFF
GO
SET IDENTITY_INSERT [dbo].[Telefonos] ON 

INSERT [dbo].[Telefonos] ([id], [telefono], [id_tipo]) VALUES (1, N'123456789', 1)
SET IDENTITY_INSERT [dbo].[Telefonos] OFF
GO
SET IDENTITY_INSERT [dbo].[Tematicas] ON 

INSERT [dbo].[Tematicas] ([id], [tematica]) VALUES (1, N'Fútbol')
INSERT [dbo].[Tematicas] ([id], [tematica]) VALUES (2, N'Entrenamiento')
SET IDENTITY_INSERT [dbo].[Tematicas] OFF
GO
SET IDENTITY_INSERT [dbo].[TiposUsuarios] ON 

INSERT [dbo].[TiposUsuarios] ([id], [tipo]) VALUES (1, N'ADMIN')
INSERT [dbo].[TiposUsuarios] ([id], [tipo]) VALUES (2, N'usuario')
INSERT [dbo].[TiposUsuarios] ([id], [tipo]) VALUES (3, N'empresa')
SET IDENTITY_INSERT [dbo].[TiposUsuarios] OFF
GO
SET IDENTITY_INSERT [dbo].[TipoTelefonos] ON 

INSERT [dbo].[TipoTelefonos] ([id], [tipo]) VALUES (1, N'Móvil')
INSERT [dbo].[TipoTelefonos] ([id], [tipo]) VALUES (2, N'Fijo')
SET IDENTITY_INSERT [dbo].[TipoTelefonos] OFF
GO
SET IDENTITY_INSERT [dbo].[Usuarios] ON 

INSERT [dbo].[Usuarios] ([id], [id_persona], [id_tipouser], [correo], [passwrd], [id_empresa]) VALUES (1, 1, 2, N'ronaldoo@gmail.com', N'ronaldo123', NULL)
INSERT [dbo].[Usuarios] ([id], [id_persona], [id_tipouser], [correo], [passwrd], [id_empresa]) VALUES (2, 2, 2, N'gaucho@gmail.com', N'tiberius321', NULL)
INSERT [dbo].[Usuarios] ([id], [id_persona], [id_tipouser], [correo], [passwrd], [id_empresa]) VALUES (3, 3, 2, N'pele@gmail.com', N'pele123', NULL)
INSERT [dbo].[Usuarios] ([id], [id_persona], [id_tipouser], [correo], [passwrd], [id_empresa]) VALUES (4, 4, 2, N'zico@gmail.com', N'zico123', NULL)
INSERT [dbo].[Usuarios] ([id], [id_persona], [id_tipouser], [correo], [passwrd], [id_empresa]) VALUES (5, 6, 1, N'lollespartam@gmail.com', N'ADMIN', NULL)
INSERT [dbo].[Usuarios] ([id], [id_persona], [id_tipouser], [correo], [passwrd], [id_empresa]) VALUES (6, 7, 1, N'elpanadero@gmail.com', N'ADMIN', NULL)
INSERT [dbo].[Usuarios] ([id], [id_persona], [id_tipouser], [correo], [passwrd], [id_empresa]) VALUES (7, NULL, 3, N'saopaulodepostes@gmail.com', N'saopaulo123', 1)
INSERT [dbo].[Usuarios] ([id], [id_persona], [id_tipouser], [correo], [passwrd], [id_empresa]) VALUES (8, 8, 2, N'salomon@gmail.com', N'salomon123', NULL)
INSERT [dbo].[Usuarios] ([id], [id_persona], [id_tipouser], [correo], [passwrd], [id_empresa]) VALUES (9, 9, 2, N'angela@gmail.com', N'1231231231', NULL)
INSERT [dbo].[Usuarios] ([id], [id_persona], [id_tipouser], [correo], [passwrd], [id_empresa]) VALUES (10, 10, 2, N'isma@gmail.com', N'isma123', NULL)
SET IDENTITY_INSERT [dbo].[Usuarios] OFF
GO
SET IDENTITY_INSERT [dbo].[Voluntarios] ON 

INSERT [dbo].[Voluntarios] ([id], [id_escuela], [id_persona]) VALUES (1, 1, 1)
INSERT [dbo].[Voluntarios] ([id], [id_escuela], [id_persona]) VALUES (2, 2, 2)
INSERT [dbo].[Voluntarios] ([id], [id_escuela], [id_persona]) VALUES (3, 3, 3)
SET IDENTITY_INSERT [dbo].[Voluntarios] OFF
GO
ALTER TABLE [dbo].[Asociacion]  WITH CHECK ADD FOREIGN KEY([id_empresa])
REFERENCES [dbo].[Empresas] ([id])
GO
ALTER TABLE [dbo].[Asociacion]  WITH CHECK ADD FOREIGN KEY([id_escuela])
REFERENCES [dbo].[Escuelas] ([id])
GO
ALTER TABLE [dbo].[Calles]  WITH CHECK ADD FOREIGN KEY([id_colonia])
REFERENCES [dbo].[Colonias] ([id])
GO
ALTER TABLE [dbo].[Colonias]  WITH CHECK ADD FOREIGN KEY([id_municipio])
REFERENCES [dbo].[Municipios] ([id])
GO
ALTER TABLE [dbo].[Convocatorias]  WITH CHECK ADD FOREIGN KEY([id_empresa])
REFERENCES [dbo].[Empresas] ([id])
GO
ALTER TABLE [dbo].[Convocatorias]  WITH CHECK ADD FOREIGN KEY([id_estatus])
REFERENCES [dbo].[ConvocatoriasEstatus] ([id])
GO
ALTER TABLE [dbo].[Convocatorias]  WITH CHECK ADD FOREIGN KEY([id_tematica])
REFERENCES [dbo].[Tematicas] ([id])
GO
ALTER TABLE [dbo].[Direcciones]  WITH CHECK ADD FOREIGN KEY([id_calle])
REFERENCES [dbo].[Calles] ([id])
GO
ALTER TABLE [dbo].[Direcciones]  WITH CHECK ADD FOREIGN KEY([id_colonia])
REFERENCES [dbo].[Colonias] ([id])
GO
ALTER TABLE [dbo].[Direcciones]  WITH CHECK ADD FOREIGN KEY([id_estado])
REFERENCES [dbo].[Estados] ([id])
GO
ALTER TABLE [dbo].[Direcciones]  WITH CHECK ADD FOREIGN KEY([id_municipio])
REFERENCES [dbo].[Municipios] ([id])
GO
ALTER TABLE [dbo].[Escuelas]  WITH CHECK ADD FOREIGN KEY([id_direccion])
REFERENCES [dbo].[Direcciones] ([id])
GO
ALTER TABLE [dbo].[Municipios]  WITH CHECK ADD FOREIGN KEY([id])
REFERENCES [dbo].[Estados] ([id])
GO
ALTER TABLE [dbo].[Voluntarios]  WITH CHECK ADD FOREIGN KEY([id_escuela])
REFERENCES [dbo].[Escuelas] ([id])
GO
ALTER TABLE [dbo].[Voluntarios]  WITH CHECK ADD FOREIGN KEY([id_persona])
REFERENCES [dbo].[Personas] ([id])
GO
/****** Object:  StoredProcedure [dbo].[sp_ingresarUsuario]    Script Date: 8/1/2024 7:55:45 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[sp_ingresarUsuario]
	@nombre VARCHAR(150),
	@apellidop VARCHAR(150),
	@apellidom VARCHAR(150),
	@correo VARCHAR(150),
	@password VARCHAR(25)
AS
BEGIN
	BEGIN TRANSACTION
	BEGIN TRY
	
		INSERT INTO Personas (nombre, apellidop, apellidom) 
		VALUES (@nombre, @apellidop, @apellidom)

		DECLARE @idtipo INT
		DECLARE @idper INT
		SET @idtipo = 2
		SET @idper = SCOPE_IDENTITY()

		INSERT INTO Usuarios (id_persona, id_tipouser, correo, passwrd)
		VALUES (@idper, @idtipo, @correo, @password)
	COMMIT TRANSACTION
	END TRY
	BEGIN CATCH
ROLLBACK TRANSACTION;
DECLARE @ErrorMessage NVARCHAR(4000);
SET @ErrorMessage = ERROR_MESSAGE();
PRINT @ErrorMessage;
END CATCH;
END;
GO
USE [master]
GO
ALTER DATABASE [TerraForce] SET  READ_WRITE 
GO
