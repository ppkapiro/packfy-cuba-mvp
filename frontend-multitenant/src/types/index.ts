// Tipos para React global
export type FC<Props = Record<string, never>> = React.FunctionComponent<Props>;
export type ChangeEvent<T = Element> = React.ChangeEvent<T>;

// Tipos para Multitenancy
export interface Empresa {
  id: number;
  name: string;
  slug: string;
  domain_url: string;
  schema_name: string;
  description?: string;
  logo?: string;
  email: string;
  phone?: string;
  address?: string;
  created_at: string;
  updated_at: string;
  rol?: string; // Agregado para el rol del usuario en la empresa
  perfiles?: PerfilUsuario[]; // Agregado para los perfiles del usuario en la empresa
}

export interface PerfilUsuario {
  id: number;
  usuario: string;
  rol:
    | "dueno"
    | "operador_miami"
    | "operador_cuba"
    | "remitente"
    | "destinatario";
  empresa: number;
  fecha_ingreso?: string;
  configuracion?: Record<string, any>;
}

// Tipos para la API de Envíos

export interface Envio {
  id: string;
  numero_guia: string;
  descripcion: string;
  peso: number;
  valor_declarado: number;

  remitente_nombre: string;
  remitente_direccion: string;
  remitente_telefono: string;
  remitente_email: string | null;

  destinatario_nombre: string;
  destinatario_direccion: string;
  destinatario_telefono: string;
  destinatario_email: string | null;

  estado_actual: string;
  estado_display?: string;
  fecha_creacion: string;
  fecha_estimada_entrega: string | null;
  ultima_actualizacion: string;

  notas: string | null;
  historial?: HistorialEstado[];
  creado_por?: Usuario | null;
  actualizado_por?: Usuario | null;
}

export interface HistorialEstado {
  id: string;
  envio: string;
  estado_anterior: string;
  estado_nuevo: string;
  estado_anterior_display: string;
  estado_nuevo_display: string;
  fecha_cambio: string;
  notas: string | null;
  usuario: string | null;
}

export interface EnvioFormData {
  numero_guia: string;
  descripcion: string;
  peso: number;
  alto: number;
  ancho: number;
  largo: number;
  valor_declarado: number;

  remitente_nombre: string;
  remitente_direccion: string;
  remitente_telefono: string;
  remitente_email?: string;

  destinatario_nombre: string;
  destinatario_direccion: string;
  destinatario_telefono: string;
  destinatario_email?: string;

  fecha_entrega_estimada?: string;
  notas?: string;
}

// Tipos para la API de Usuarios

export interface Usuario {
  id: number;
  email: string;
  nombre: string;
  apellidos: string;
  telefono?: string;
  cargo?: string;
  is_active: boolean;
  fecha_registro: string;
  ultima_actualizacion: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface AuthResponse {
  access: string;
  refresh: string;
}

// Tipos para la API de Empresas

export interface Empresa {
  id: number;
  name: string;
  domain_url: string;
  schema_name: string;
  description?: string;
  logo?: string;
  email: string;
  phone?: string;
  address?: string;
  created_at: string;
  updated_at: string;
}

export interface EmpresaFormData {
  name: string;
  domain_url: string;
  schema_name: string;
  description?: string;
  logo?: File;
  email: string;
  phone?: string;
  address?: string;
  admin_email: string;
  admin_password: string;
  admin_nombre: string;
  admin_apellidos: string;
}
