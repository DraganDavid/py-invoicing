from typing import List
from datetime import date
from sqlalchemy import String, create_engine, delete, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from sqlalchemy import select


class Base(DeclarativeBase):
    pass

class Factura(Base):
    __tablename__ = "factura"
    id: Mapped[int] = mapped_column(primary_key=True)
    id_client: Mapped[int] = mapped_column(ForeignKey("client.id"))
    client: Mapped["Client"] = relationship(back_populates="factura_client", foreign_keys=[id_client])
    id_furnizor: Mapped[int] = mapped_column(ForeignKey("client.id"))
    furnizor: Mapped["Client"] = relationship(back_populates="factura_furnizor",foreign_keys=[id_furnizor])
    produse: Mapped[List["Produs"]] = relationship(back_populates="factura")
    total: Mapped[int]


class Client(Base):
    __tablename__ = "client"
    id: Mapped[int] = mapped_column(primary_key=True)
    nume_client: Mapped[str]
    cui_client = Mapped[int]
    adresa_client: Mapped[str]
    factura_client: Mapped["Factura"] = relationship(back_populates="client", foreign_keys="Factura.id_client")
    factura_furnizor: Mapped["Factura"] = relationship(back_populates="furnizor", foreign_keys="Factura.id_furnizor")


class Produs(Base):
    __tablename__ = "produs"
    id: Mapped[int] = mapped_column(primary_key=True)
    denumire: Mapped[str]
    cantitate: Mapped[int]
    pret_unitar: Mapped[int]
    pret_total: Mapped[int]
    factura_id: Mapped[int] = mapped_column(ForeignKey("Factura.id"))
    factura: Mapped["Factura"] = relationship(back_populates="produse")

engine = create_engine("sqlite://", echo=True)
Base.metadata.create_all(engine)

x = True
while x:
    print("1 - Introduceti client nou!")
    print("2 - Introduceti un produs nou!")
    print("3 - Elibereaza o factura!")
    print("4 - Sterge un client!")
    print("5 - Sterge un produs!")
    print("6 - Iesi din program!")
    optiune = int(input("Apasati numarul actiunii dorite!"))
    if optiune == 1:
        nume_client = input("Introduceti numele clientului!")
        cui_client = int(input("Introduceti CUI-ul clientului"))
        adresa_client = input("Introduceti adresa clientului")
        with Session(engine) as session:
            c = Client(
                nume_client=nume_client,
                cui_client=cui_client,
                adresa_client=adresa_client
            )
            session.add(c)
            session.commit()
        print(f"A fost introdus clientul cu numele {nume_client}, CUI-ul {cui_client}, si adresa {adresa_client}")
    if optiune == 2:
        denumire_produs = input("Introduceti numele produsului!")
        cantitate_produs = input("Introduceti cantitatea de unitati/kg/litri a produsului!")
        pret_unitar_produs = int(input("Introduceti pretul unitar al produsului!"))
        with Session(engine) as session:
            p = Produs(
                denumire=denumire_produs,
                cantitate=cantitate_produs,
                pret_unitar=pret_unitar_produs
            )
            session.add(p)
            session.commit()
    if optiune == 3:
        furnizor_factura = input("Introduceti numele furnizorului dintre clientii existenti!")
        adresa_furnizor = select(Client.adresa_client).where(Client.nume_client.has(furnizor_factura))
        client_factura = input("Introduceti numele clientului catre cumpara produsul sau produsele!")
        adresa_client = select(Client.adresa_client).where(Client.nume_client.has(client_factura))
        nr_produse = int(input("Introduceti numarul produselor care vor fi trecute pe factura!"))
        lista = []
        for i in range (nr_produse):
            produs = input("Introdu numele produsului")
            lista.append(produs)
        with open("factura.txt") as f:
            f.write("Facutra")
            f.write(f"Data emiterii: {date.today()}")
            f.write(f"Numarul Facturii: {Factura.nr_facutra}")
            f.write("Furnizor:")
            f.write(f"CUI Furnizor: {Factura.furnizor.cui_client}")
            f.write(f"Nume Furnizor: {Factura.furnizor.nume_client}")
            f.write(f"Adresa Furnizor: {Factura.furnizor.adresa_client} ")
            f.write("Client:")
            f.write(f"CUI Client: {Factura.client.cui_client}")
            f.write(f"Nume Client: {Factura.client.nume_client}")
            f.write(f"Adresa Client: {Factura.client.adresa_client} ")
            f.write("Produse: ")
            total_facutra = 0
            for produs in lista:
                p = Produs()
                f.write(f"{produs} ... Cantitate: {cantitate_produs} ... Pret unitar: {pret_unitar_produs} ... Pret total pentru acest produs: {cantitate_produs * pret_unitar_produs}")
                total_facutra += pret_unitar_produs * cantitate_produs
            f.write(f"Total plata: {total_facutra}")
    if optiune == 4:
        client_de_sters = input("Introduceti CUI-ul clientului pe care doriti sa il stergeti!")
        stmt = delete(Client).where(Client.cui_client == client_de_sters)
        print(stmt)
    if optiune == 5:
        produs_de_sters = input("Introduceti numele produsului pe care doriti sa il stergeti!")
        stmt = delete(Produs).where(Produs.denumire == produs_de_sters)
        print(stmt)
    if optiune == 6:
        print("Ati iesit din program!")
        x = False