import { describe, it, expect, vi, beforeEach } from "vitest";
import { enviosAPI, authAPI, empresasAPI } from "../services/api";

// Mock fetch global
const mockFetch = vi.fn();
global.fetch = mockFetch;

// Mock console methods para evitar logs en tests
vi.spyOn(console, "log").mockImplementation(() => {});
vi.spyOn(console, "error").mockImplementation(() => {});

describe("API Services", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();

    // Mock successful response by default
    mockFetch.mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({ data: "test" }),
      text: async () => "success",
    });
  });

  describe("authAPI", () => {
    it("debe hacer login correctamente", async () => {
      const mockResponse = {
        access: "mock-access-token",
        refresh: "mock-refresh-token",
        user: { id: 1, username: "testuser" },
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => mockResponse,
      });

      const result = await authAPI.login("testuser", "password123");

      expect(mockFetch).toHaveBeenCalledWith(
        expect.stringContaining("/auth/login/"),
        expect.objectContaining({
          method: "POST",
          headers: expect.objectContaining({
            "Content-Type": "application/json",
          }),
          body: JSON.stringify({
            username: "testuser",
            password: "password123",
          }),
        })
      );

      expect(result.data).toEqual(mockResponse);
    });

    it("debe manejar errores de login", async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 401,
        json: async () => ({ detail: "Invalid credentials" }),
      });

      const result = await authAPI.login("wrong", "credentials");

      expect(result.error).toBeDefined();
      expect(result.status).toBe(401);
    });

    it("debe hacer logout correctamente", async () => {
      localStorage.setItem("access_token", "test-token");

      const result = await authAPI.logout();

      expect(result.status).toBe(200);
      expect(localStorage.getItem("access_token")).toBeNull();
    });
  });

  describe("enviosAPI", () => {
    beforeEach(() => {
      localStorage.setItem("access_token", "test-access-token");
    });

    it("debe obtener todos los envíos con paginación", async () => {
      const mockEnvios = {
        results: [
          { id: 1, numero_guia: "PK001", estado_actual: "PENDIENTE" },
          { id: 2, numero_guia: "PK002", estado_actual: "EN_TRANSITO" },
        ],
        count: 2,
        next: null,
        previous: null,
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => mockEnvios,
      });

      const result = await enviosAPI.getAll(1, 10);

      expect(mockFetch).toHaveBeenCalledWith(
        expect.stringContaining("/envios/?page=1&page_size=10"),
        expect.objectContaining({
          method: "GET",
          headers: expect.objectContaining({
            Authorization: "Bearer test-access-token",
          }),
        })
      );

      expect(result.data).toEqual(mockEnvios);
    });

    it("debe crear un nuevo envío", async () => {
      const nuevoEnvio = {
        remitente_nombre: "Juan Pérez",
        destinatario_nombre: "María García",
        descripcion: "Paquete de prueba",
        peso: 2.5,
      };

      const mockResponse = {
        id: 1,
        numero_guia: "PK001",
        ...nuevoEnvio,
        estado_actual: "PENDIENTE",
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 201,
        json: async () => mockResponse,
      });

      const result = await enviosAPI.create(nuevoEnvio);

      expect(mockFetch).toHaveBeenCalledWith(
        expect.stringContaining("/envios/"),
        expect.objectContaining({
          method: "POST",
          headers: expect.objectContaining({
            "Content-Type": "application/json",
            Authorization: "Bearer test-access-token",
          }),
          body: JSON.stringify(nuevoEnvio),
        })
      );

      expect(result.data).toEqual(mockResponse);
    });

    it("debe obtener un envío por ID", async () => {
      const mockEnvio = {
        id: 1,
        numero_guia: "PK001",
        estado_actual: "PENDIENTE",
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => mockEnvio,
      });

      const result = await enviosAPI.getById(1);

      expect(mockFetch).toHaveBeenCalledWith(
        expect.stringContaining("/envios/1/"),
        expect.objectContaining({
          method: "GET",
          headers: expect.objectContaining({
            Authorization: "Bearer test-access-token",
          }),
        })
      );

      expect(result.data).toEqual(mockEnvio);
    });

    it("debe obtener envío por número de guía", async () => {
      const mockResponse = {
        numero_guia: "PK001",
        estado_actual: "EN_TRANSITO",
        remitente_nombre: "Juan Pérez",
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => mockResponse,
      });

      const result = await enviosAPI.getByGuia("PK001");

      expect(mockFetch).toHaveBeenCalledWith(
        expect.stringContaining("/envios/"),
        expect.objectContaining({
          method: "GET",
          headers: expect.objectContaining({
            Authorization: "Bearer test-access-token",
          }),
        })
      );

      expect(result.data).toEqual(mockResponse);
    });
  });

  describe("empresasAPI", () => {
    beforeEach(() => {
      localStorage.setItem("access_token", "test-access-token");
    });

    it("debe obtener todas las empresas", async () => {
      const mockEmpresas = {
        results: [
          { id: 1, nombre: "Empresa Test 1" },
          { id: 2, nombre: "Empresa Test 2" },
        ],
        count: 2,
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => mockEmpresas,
      });

      const result = await empresasAPI.getAll();

      expect(result.data).toEqual(mockEmpresas);
    });
  });

  describe("Error Handling", () => {
    it("debe manejar errores de red", async () => {
      mockFetch.mockRejectedValueOnce(new Error("Network error"));

      const result = await enviosAPI.getAll();

      expect(result.error).toBeDefined();
      expect(result.status).toBe(500);
    });

    it("debe manejar respuestas con error HTTP", async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 404,
        json: async () => ({ detail: "Not found" }),
        text: async () => "Not found",
      });

      const result = await enviosAPI.getById(999);

      expect(result.error).toBeDefined();
      expect(result.status).toBe(404);
    });
  });
});
