const generarId = () => {
    const random = Math.random().toString(10).substring(2);
    const fecha = Date.now().toString(10);
    return random + fecha
}
export default generarId;