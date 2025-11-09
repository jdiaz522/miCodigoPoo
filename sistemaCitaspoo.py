from abc import ABC, abstractmethod
import numpy as np
import pandas as pd

charsVal = "abcdefghijklmnñopqrstuvxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ "


class SystemSpa:
    def __init__(self, nombre):
        self.__nombre = nombre
        self.__terapeutas = []
        self.__cabinas = []
        self.__servicios = []
        self.__citas = []

    def validarNomb(self, nombre="nombre"):
        while True:
            nombreCl = input(f"Ingrese el {nombre}: ").strip()
            esValid = True
            if not nombreCl:
                print("El nombre no puede estar vacío.")
                esValid = False
            else:
                for char in nombreCl:
                    if char not in charsVal:
                        print(f"Error: El caracter '{char}' no es válido.")
                        esValid = False
                        break
            if esValid:
                return nombreCl
            else:
                print("Por favor, ingrese un nombre solo con letras y espacios.")

    def validarDate(self):
        while True:
            fechaStr = input("Ingrese la fecha (DD-MM-AAAA): ").strip()
            if len(fechaStr) == 10 and fechaStr[2] == "-" and fechaStr[5] == "-":
                try:
                    diaStr, mesStr, anioStr = fechaStr.split("-")
                    dia = int(fechaStr[0:2])
                    mes = int(fechaStr[3:5])
                    anio = int(fechaStr[6:10])

                    if not 1 <= dia <= 31:
                        print("Error: El día debe estar entre 01 y 31.")
                    elif not 1 <= mes <= 12:
                        print("Error: El mes debe estar entre 01 y 12.")
                    elif not 2025 <= anio <= 2030:
                        print(f"Error: El año {anio} no es válido.")
                    else:
                        return fechaStr

                except ValueError:
                    print("La fecha debe contener números y guiones (DD-MM-AAAA).")
            else:
                print("Formato inválido. Debe ser DD-MM-AAAA (ej. 25-10-2025)")

    def selecServs(self):
        self.listarServ()
        servsSol = []
        duracTot = 0
        while True:
            serviNom = input("Ingrese servicio (o 'fin' para terminar): ").capitalize()
            if serviNom.lower() == "fin":
                if not servsSol:
                    print("La cita debe tener por lo menos un servicio")
                    continue
                else:
                    break

            encont = None
            for servicio in self.servicios:
                if serviNom == servicio.nombre:
                    servsSol.append(servicio)
                    duracTot += servicio.duracion
                    encont = servicio
                    print(f"Servicio '{servicio.nombre}' agregado.")
                    break

            if not encont:
                print(f"No se encontró el servicio '{serviNom}'.")
        return servsSol, duracTot

    def validarHora(self, duracTot):
        print(f"Duración total de la cita: {duracTot}h")
        print("Horario de atención: 9:00 - 19:00")
        while True:
            try:
                maxHorIni = 19 - duracTot
                horIni = int(
                    input("Ingrese hora de inicio (entero " f"entre 9 y {maxHorIni}): ")
                )
                horFin = horIni + duracTot
                if horIni < 9:
                    print("Error: La hora de inicio debe ser a las 9 o después.")
                elif horFin > 19:
                    print(
                        f"Error: La cita terminaría a las {horFin}:"
                        "00, excede las 19:00."
                    )
                else:
                    return horIni, horFin
            except ValueError:
                print("El valor ingresado no es válido.")

    def registCab(self, cabina):
        if isinstance(cabina, Cabina):
            self.__cabinas.append(cabina)
            print(
                f"Cabina {cabina.codigo} habilitada para el servicio de {cabina.area}"
            )

    def registTerap(self, terapeuta):
        if isinstance(terapeuta, Terapeuta):
            self.__terapeutas.append(terapeuta)
            print(
                f"Terapeuta {terapeuta.nombre} con código {terapeuta.codigo} agregado."
            )

    def registServ(self, servicio):
        if isinstance(servicio, Servicio):
            self.__servicios.append(servicio)
            print(f"Servicio de {servicio.nombre} registrado")

    def listarServ(self):
        print("\n--- Servicios Disponibles ---")
        for serv in self.__servicios:
            print(serv)
        print("-----------------------------\n")

    def agendarCita(self):
        print("\n--- Agendar Nueva Cita ---")
        nombreCl = self.validarNomb("nombre del cliente").title()
        if nombreCl is None:
            return

        fechaStr = self.validarDate()
        if fechaStr is None:
            return

        self.listarServ()
        servsSol, duracTot = self.selecServs()
        if not servsSol:
            print("No se seleccionaron servicios. Cancelando cita")
            return

        horIni, horFin = self.validarHora(duracTot)

        nuevaCita = Cita(nombreCl, horIni, fechaStr, servsSol)

        self.__citas.append(nuevaCita)
        print(f"\nCita {nuevaCita.codigo} registrada con éxito. Estado: Pendiente.")
        print("Use la Opción 6 del menú para asignar terapeuta y cabinas.")

    def buscaCitaCod(self):
        codCita = (
            input("Ingrese el código de la cita (ej. A001, 0 para volver): ")
            .upper()
            .strip()
        )
        if codCita == "0":
            return None
        for cita in self.__citas:
            if cita.codigo == codCita:
                return cita

        print(f"Error: No se encontró la cita con código {codCita}.")
        return None

    def selecRecurso(self, listaDisp, tipoRecurso, permiteCero=False):
        while True:
            try:
                prompt = f"Seleccione el número del {tipoRecurso}: "
                if permiteCero is True:
                    prompt = f"Seleccione el número del {tipoRecurso} (0 para saltar): "
                op = int(input(prompt))
                if permiteCero is True and op == 0:
                    return None
                if op >= 1 and op <= len(listaDisp):
                    return listaDisp[op - 1]
                else:
                    print("Número fuera de rango.")
            except ValueError:
                print("Entrada no válida.")

    def asignaRecursos(self):
        print("\n--- Asignación de Recursos (Paso 2) ---")
        cita = self.buscaCitaCod()
        if cita is None:
            return
        if cita.estado == "Finalizada":
            print(f"La cita {cita.codigo} ya está finalizada. No se puede modificar.")
            return
        print(f"\nCita seleccionada: {cita.codigo} - {cita.estado}")
        print(cita)

        while True:
            print("\nOpciones de Asignación:")
            print("1. Asignar Terapeuta (cita completa)")
            print("2. Asignar Cabinas (por bloque)")
            print("3. Volver al menú principal")
            op = input("Ingrese su opción: ")
            if op == "1":
                self.asignaTerapCita(cita)
            elif op == "2":
                self.asignaCabBloques(cita)
            elif op == "3":
                break
            else:
                print("Opción no válida")

    def asignaTerapCita(self, cita):
        if cita.terapAsig is not None:
            print(f"Esta cita ya tiene un terapeuta asignado: {cita.terapAsig.nombre}")
            return
        print(f"\nBuscando terapeutas disponibles para {cita.codigo}...")
        listaDisp = []
        for ter in self.__terapeutas:
            if ter.tieneCupo(cita.fecha) is False:
                continue
            if ter.estaDisp(cita.fecha, cita.bloques):
                listaDisp.append(ter)
        if len(listaDisp) == 0:
            print(
                "No hay terapeutas disponibles para el horario completo de esta cita."
            )
            return
        print("Terapeutas Disponibles:")
        for i, ter in enumerate(listaDisp, start=1):
            print(f"  {i}. {ter.codigo} - {ter.nombre}")
        terElegido = self.selecRecurso(listaDisp, "terapeuta")
        if terElegido is not None:
            cita.asignaTerap(terElegido)
            terElegido.agregarCita(cita)

    def asignaCabBloques(self, cita):
        print("\n--- Asignación de Cabinas por Bloque ---")
        for i, bloque in enumerate(cita.bloques):
            serv = bloque["servicio"]
            print(
                f"\nBloque {i + 1}: {serv.nombre} ("
                f"{bloque['horIni']}:00–{bloque['horFin']}:00)"
            )

            if bloque["cabina"] is not None:
                print(f"  -> Cabina ya asignada: {bloque['cabina'].codigo}")
                continue
            listaDisp = []
            for cab in self.__cabinas:
                if cab.dispParaServ(cita.fecha, bloque):
                    listaDisp.append(cab)

            if len(listaDisp) == 0:
                print(
                    f"  -> ¡Alerta! No hay cabinas de tipo '{serv.nombre}' "
                    "disponibles para este bloque. No asignada."
                )
                continue
            print("  Cabinas Disponibles para este bloque:")
            for j, cab in enumerate(listaDisp, start=1):
                print(f"    {j}. {cab.codigo} (Área: {cab.area})")
            cabElegida = self.selecRecurso(listaDisp, "cabina", True)
            if cabElegida is not None:
                cita.asignaCabBloq(i, cabElegida)
                cabElegida.agregarCita(cita)
        print("\nAsignación de cabinas completada.")

    @property
    def nombre(self):
        return self.__nombre

    @property
    def terapeutas(self):
        return self.__terapeutas

    @property
    def servicios(self):
        return self.__servicios

    @property
    def cabinas(self):
        return self.__cabinas

    def __str__(self):
        return (
            f"Bienvenido. Este es el sistema de gestión de citas de {self.__nombre} Spa"
        )


class Recurso(ABC):
    def __init__(self):
        self.__agenda = {}

    @property
    @abstractmethod
    def codigo(self):
        pass

    def getCitasDia(self, fecha):
        return self.__agenda.get(fecha, [])

    def estaDisp(self, fecha, bloquesNuevos):
        citasDia = self.getCitasDia(fecha)

        for citaExist in citasDia:
            for blExist in citaExist.bloques:
                for blNuevo in bloquesNuevos:
                    if seSolapan(
                        blNuevo["horIni"],
                        blNuevo["horFin"],
                        blExist["horIni"],
                        blExist["horFin"],
                    ):
                        return False
        return True

    def agregarCita(self, cita):
        fecha = cita.fecha
        if fecha not in self.__agenda:
            self.__agenda[fecha] = []
        self.__agenda[fecha].append(cita)
        print(f"Cita {cita.codigo} agregada a la agenda de {self.codigo} el {fecha}")

    def removerCita(self, removerCita):
        fecha = removerCita.fecha
        if fecha in self.__agenda:
            citasDia = self.__agenda[fecha]
            citasAct = []
            for citaExist in citasDia:
                if citaExist.codigo != removerCita.codigo:
                    citasAct.append(citaExist)
            self.__agenda[fecha] = citasAct
            print(f"Cita {removerCita.codigo} removida de la agenda.")


class Terapeuta(Recurso):
    __registTer = 0

    def __init__(self, nombre):
        Terapeuta.__registTer += 1
        super().__init__()
        self.__citAtend = 0
        self.__nombre = nombre
        self.__codigo = f"T{Terapeuta.__registTer:03d}"

    @property
    def nombre(self):
        return self.__nombre

    @property
    def citAtend(self):
        return self.__citAtend

    @property
    def codigo(self):
        return self.__codigo

    def tieneCupo(self, fecha):
        citasDia = self.getCitasDia(fecha)
        if len(citasDia) < 6:
            return True
        else:
            print(f"Aviso: Terapeuta {self.nombre} ya tiene 6 citas el {fecha}.")
            return False

    def citCantPlus(self):
        self.__citAtend += 1

    def __str__(self):
        return f"{self.nombre} es un Terapeuta con código {self.codigo}"


class Cabina(Recurso):
    __registCab = 0

    def __init__(self, area):
        super().__init__()
        Cabina.__registCab += 1
        self.__codigo = f"C{Cabina.__registCab:03d}"
        self.__area = area

    @property
    def area(self):
        return self.__area

    @property
    def codigo(self):
        return self.__codigo

    def dispParaServ(self, fecha, bloque):
        servReq = bloque["servicio"]
        if self.area != servReq.nombre:
            return False
        return super().estaDisp(fecha, [bloque])

    def __str__(self):
        return f"Cabina {self.codigo}, habilitada para {self.area}"


class Servicio:
    __registServ = 0

    def __init__(self, nombre, duracion, precio):
        self.__nombre = nombre
        self.__duracion = duracion
        self.__precio = precio

        Servicio.__registServ += 1

    @property
    def nombre(self):
        return self.__nombre

    @property
    def duracion(self):
        return self.__duracion

    @property
    def precio(self):
        return self.__precio

    @property
    def cantServ(self):
        return self.__registServ

    def __str__(self):
        return (
            f"- {self.__nombre} | Duración: {self.__duracion}h | "
            f"Precio: S/{self.__precio:.2f}"
        )


class Cita:
    __registCit = 0

    def __init__(self, nombreCl, horIni, fechaStr, listaServs):
        self.__nombreCl = nombreCl
        self.__fecha = fechaStr
        self.__estado = "Pendiente"
        self.__terapAsig = None
        self.__bloques = []

        Cita.__registCit += 1
        self.__codigo = f"A{Cita.__registCit:03d}"

        self.armarBloques(listaServs, horIni)

        self.__precio = self.calcuPrecio()

    def calcuPrecio(self):
        total = 0
        for bloque in self.__bloques:
            total += bloque["servicio"].precio
        return total

    def armarBloques(self, listaServs, horIni):
        horaActual = horIni
        self.__bloques = []
        for serv in listaServs:
            dur = serv.duracion
            bloque = {
                "servicio": serv,
                "horIni": horaActual,
                "horFin": horaActual + dur,
                "cabina": None,
            }
            self.__bloques.append(bloque)
            horaActual = bloque["horFin"]

    def asignaTerap(self, terapeuta):
        if isinstance(terapeuta, Terapeuta):
            self.__terapAsig = terapeuta
            self.__estado = "Agendada"

    def asignCabBloq(self, indiceBloq, cabina):
        if indiceBloq >= 0:
            if indiceBloq < len(self.__bloques):
                if isinstance(cabina, Cabina):
                    self.__bloques[indiceBloq]["cabina"] = cabina

    def finalizarCit(self):
        self.__estado = "Finalizada"

    @property
    def codigo(self):
        return self.__codigo

    @property
    def nombreCl(self):
        return self.__nombreCl

    @property
    def fecha(self):
        return self.__fecha

    @property
    def bloques(self):
        return self.__bloques

    @property
    def estado(self):
        return self.__estado

    @property
    def terapAsig(self):
        return self.__terapAsig

    @property
    def horIni(self):
        if len(self.__bloques) > 0:
            return self.__bloques[0]["horIni"]
        return 0

    @property
    def horaFinal(self):
        if len(self.__bloques) > 0:
            return self.__bloques[-1]["horFin"]
        return 0

    @property
    def precio(self):
        return self.__precio

    def __str__(self):
        encabezado = f"--- Cita {self.codigo} [Estado: {self.estado}] ---"
        cliente = f"Cliente: {self.nombreCl}"
        horario = f"Fecha: {self.fecha} | Hora: {self.horIni}:00 - {self.horaFinal}:00"

        terapStr = "Terapeuta: N/A"
        if self.terapAsig is not None:
            terapStr = f"Terapeuta: {self.terapAsig.nombre}"

        servStr = "Bloques de Servicios:\n"
        for i, bloque in enumerate(self.__bloques, start=1):
            serv = bloque["servicio"]
            cab = bloque["cabina"]

            cabStr = "N/A"
            if cab is not None:
                cabStr = cab.codigo
            servStr += (
                f"  {i}. {serv.nombre} ({bloque['horIni']}:00–{bloque['horFin']}:00) "
                f"| Cabina: {cabStr}\n"
            )

        return (
            f"{encabezado}\n{cliente}\n{horario}\n{terapStr}\n"
            f"{servStr}"
            f"--------------------"
        )


def menuPrincipal():
    while True:
        try:
            print("MENU PRINCIPAL")
            print("1. Registrar cabina")
            print("2. Registrar terapeuta")
            print("3. Listar servicios")
            print("4. Agregar servicios")
            print("5. Agendar cita")
            print("6. Asignar Recursos a Cita")
            print("7. Finalizar cita")
            print("8. Ver reportes")
            print("9. Opción en proceso...")
            print("10. Salir")

            opcion = int(input("Ingrese el número de la opción a realizar: "))
            if 1 <= opcion <= 10:
                return opcion
            print("Opción inválida. Ingrese un número del 1 al 10")
        except ValueError:
            print("Debe ingresar un número entero.")


def servsDefault(sistema):
    print("Cargando servicios predeterminados...")
    limpFacial = Servicio("Limpieza facial", 1, 50.0)
    masaje = Servicio("Masaje descontracturante", 2, 80.0)
    sauna = Servicio("Sauna", 1, 45.0)
    exfoliantes = Servicio("Exfoliación corporal", 1, 55.0)
    hidroterapia = Servicio("Hidroterapia", 2, 90.0)
    manicura = Servicio("Manicura", 1, 35.0)
    pedicura = Servicio("Pedicura", 1, 40.0)
    rutComplet = Servicio("Ruta completa", 3, 150.0)
    sistema.registServ(limpFacial)
    sistema.registServ(masaje)
    sistema.registServ(sauna)
    sistema.registServ(exfoliantes)
    sistema.registServ(hidroterapia)
    sistema.registServ(manicura)
    sistema.registServ(pedicura)
    sistema.registServ(rutComplet)
    print("Servicios predeterminados cargados correctamente.")
    print("-" * 70)


def seSolapan(ini1, fin1, ini2, fin2):
    return not (fin1 <= ini2 or ini1 >= fin2)


def main():
    miSistema = SystemSpa("Sumak")
    servsDefault(miSistema)
    print(miSistema)
    while True:
        opc = menuPrincipal()
        if opc == 1:
            miSistema.listarServ()
            area = input(
                "Ingrese el nombre del área de trabajo de "
                "la cabina (entre los servicios disponibles): "
            )
            area = area.capitalize()
            servEncont = 0
            for servicio in miSistema.servicios:
                if area == servicio.nombre:
                    servEncont = 1
                    cabina = Cabina(area)
                    miSistema.registCab(cabina)
                    break
            if servEncont == 0:
                print("No se encontró el servicio. Intente de nuevo.")

        elif opc == 2:
            nombre = miSistema.validarNomb("nombre del terapeuta").title()
            terapeuta = Terapeuta(nombre)
            miSistema.registTerap(terapeuta)

        elif opc == 3:
            miSistema.listarServ()

        elif opc == 4:
            nombre = input("Ingrese el nombre del servicio: ").capitalize()
            while True:
                try:
                    duracion = int(input("Ingrese la duración del servicio en horas: "))
                    break
                except ValueError:
                    print("No es válido")
            while True:
                try:
                    precio = float(input("Ingrese el precio del servicio: "))
                    break
                except ValueError:
                    print("No es válido")
            nuevoServ = Servicio(nombre, duracion, precio)
            miSistema.registServ(nuevoServ)

        elif opc == 5:
            miSistema.agendarCita()

        elif opc == 6:
            miSistema.asignaRecursos()
        elif opc == 7:
            print("\n--- Finalizar Cita ---")
            cita = miSistema.buscaCitaCod()
            if cita is None:
                continue

            if cita.estado == "Finalizada":
                print(f"Error: La cita {cita.codigo} ya se encuentra Finalizada.")
                continue
            if cita.estado != "Agendada":
                print(f"Error: La cita {cita.codigo} está '{cita.estado}'.")
                print("Debe asignar un terapeuta (Opción 6) antes de finalizarla.")
                continue
            cabinasCompletas = True
            for i, bloque in enumerate(cita.bloques, start=1):
                if bloque["cabina"] is None:
                    print(
                        f"Error: El Bloque {i} ({bloque['servicio'].nombre}"
                        " no tiene cabina asignada."
                    )
                    cabinasCompletas = False

            if not cabinasCompletas:
                print("Debe asignar todas las cabinas (Opción 6) antes de finalizar.")
                continue
            cita.finalizarCit()
            if cita.terapAsig:
                cita.terapAsig.citCantPlus()

            print(f"\nCita {cita.codigo} **FINALIZADA** con éxito.")
            print(f"Cliente: {cita.nombreCl}")
            print(f"Terapeuta: {cita.terapAsig.nombre}")
            print(f"Precio Total: S/{cita.precio:.2f}")

        elif opc == 8:
            print("En proceso...")
        elif opc == 9:
            print("En proceso...")
        elif opc == 10:
            print("Saliendo del sistema...")
            break


main()
