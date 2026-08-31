import '../assets/MMU.css'

function MMU() {
    return (
        <>
            <div className="MMU">
                <p>Memory Management Unit</p>
                {/* El MMU realiza dos funciones primarias:
                - traduce direcciones virtuales a direcciones fisicas
                - controla permisos de acceso de memoria */}
                {/* Las partes de un MMU son: 
                - Translation Look-aside Buffer (TLB)
                - Access control logic
                - Translation table walking logic */}
                
                {/* El MMU soporta accesos de memoria basados en:
                - Secciones: Bloques de memoria comprimidos de 1MB
                - Paginas: Small Pages consiste de bloques de memoria de 4Kb y Large Pages consiste de bloques de memoria de 64Kb */}
                
                {/*  */}

                {/* El Bufferable Bit (B) controla si la operacion de escritura puede o no utilizar el Write Buffer*/}
            </div>
        </>
    )
}

export default MMU;