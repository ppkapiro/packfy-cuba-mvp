import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { authAPI } from '../services/api';

interface User {
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

interface AuthContextData {
  token: string | null;
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

// Creamos el contexto
const AuthContext = createContext<AuthContextData>({} as AuthContextData);

// Exportamos el provider con React.memo para mejorar el rendimiento
export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Función para renovar el token
  const renovarToken = async (): Promise<boolean> => {
    try {
      const refreshToken = localStorage.getItem('refreshToken');
      if (!refreshToken) {
        console.error('No hay refresh token disponible');
        return false;
      }

      const response = await authAPI.refresh(refreshToken);
      const { access } = response.data;
      
      localStorage.setItem('token', access);
      setToken(access);
      
      console.log('Token renovado correctamente');
      return true;
    } catch (error) {
      console.error('Error al renovar el token:', error);
      return false;
    }
  };
  // Función para limpiar la sesión
  const logout = () => {
    // Limpiar tokens y estado
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
    sessionStorage.removeItem('_auth_success');
    sessionStorage.removeItem('_auth_timestamp');
    sessionStorage.removeItem('_lastEnvioSuccess');
    setToken(null);
    setUser(null);
  };

  // Función para obtener datos del usuario
  const fetchUserData = async () => {
    try {
      setIsLoading(true);
      console.log('AuthContext: Obteniendo datos del usuario...');
      const response = await authAPI.getCurrentUser();
      console.log('AuthContext: Datos del usuario obtenidos:', response.data);
      setUser(response.data as User);
    } catch (error) {
      console.error('AuthContext: Error al obtener datos del usuario:', error);
      // Si hay un error, probablemente el token expiró
      logout();
    } finally {
      setIsLoading(false);
    }
  };

  // Verificar token al cargar la aplicación
  useEffect(() => {
    const checkToken = async () => {
      // Verificar si hay un token en localStorage al cargar la página
      const storedToken = localStorage.getItem('token');
      
      if (storedToken) {
        // Establecer el token en el estado
        setToken(storedToken);
        
        try {
          // Intentar decodificar el token para verificar su validez
          const tokenParts = storedToken.split('.');
          if (tokenParts.length !== 3) {
            throw new Error('Formato de token inválido');
          }
          
          const tokenData = JSON.parse(atob(tokenParts[1]));
          const expirationTime = tokenData.exp * 1000; // Convertir a milisegundos
          
          // Si el token está a punto de expirar o ya expiró, intentar renovarlo
          if (Date.now() >= expirationTime || expirationTime - Date.now() < 300000) { // Expirado o menor a 5 minutos
            console.log('AuthContext: Token expirado o próximo a expirar, intentando renovarlo');
            const renovado = await renovarToken();
            if (!renovado) {
              console.error('AuthContext: No se pudo renovar el token');
              logout();
              setIsLoading(false);
              return;
            }
          }
          
          // Obtener la información del usuario
          await fetchUserData();
        } catch (error) {
          console.error('AuthContext: Error al verificar el token:', error);
          logout();
          setIsLoading(false);
        }
      } else {
        setIsLoading(false);
      }
    };
    
    checkToken();
  }, []);

  // Función para iniciar sesión
  const login = async (email: string, password: string) => {
    try {
      setIsLoading(true);
      console.log('Iniciando login con:', { email });
      
      const response = await authAPI.login(email, password);
      console.log('Respuesta de login:', response);
      
      // Verificar si la respuesta es exitosa
      if (response.error) {
        throw new Error(response.error);
      }
      
      const { access, refresh } = response.data as { access: string; refresh: string };
      
      // Limpiar tokens anteriores para evitar problemas
      localStorage.removeItem('token');
      localStorage.removeItem('refreshToken');
      
      // Guardar tokens nuevos
      localStorage.setItem('token', access);
      localStorage.setItem('refreshToken', refresh);
        
      // Actualizar estado
      setToken(access);
      console.log('Token guardado en localStorage');
      
      console.log('Token guardado, obteniendo datos del usuario...');
        // Obtener datos del usuario
      try {
        await fetchUserData();
        console.log('Datos del usuario obtenidos correctamente');
        
        // Añadir una señal de que la autenticación fue exitosa para ayudar en caso de problemas de navegación
        sessionStorage.setItem('_auth_success', 'true');
        sessionStorage.setItem('_auth_timestamp', new Date().toISOString());
      } catch (userError) {
        console.error('Error al obtener datos del usuario:', userError);
        // Limpiar la sesión en caso de error
        sessionStorage.removeItem('_auth_success');
        throw userError;
      }
    } catch (error) {
      console.error('Error al iniciar sesión:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AuthContext.Provider value={{
      token,
      user,
      isAuthenticated: !!token,
      isLoading,
      login,
      logout
    }}>
      {children}
    </AuthContext.Provider>
  );
};

// Definimos la función useAuth con nombre para mejorar la compatibilidad con Fast Refresh
export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth debe ser utilizado dentro de un AuthProvider');
  }
  return context;
}
