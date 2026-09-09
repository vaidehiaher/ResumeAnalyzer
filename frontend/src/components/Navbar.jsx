function Navbar() {

    const logout = () => {

        localStorage.removeItem("token");

        window.location.href = "/login";

    };

    return (

        <nav className="navbar navbar-dark bg-dark">

            <div className="container">

                <span className="navbar-brand">

                    CareerPilot AI

                </span>

                <button
                    className="btn btn-outline-light"
                    onClick={logout}
                >
                    Logout
                </button>

            </div>

        </nav>

    );
}

export default Navbar;