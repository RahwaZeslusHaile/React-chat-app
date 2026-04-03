import { useAuth } from "../contexts/AuthContext.jsx";

function Header() { 
    const { username, logout } = useAuth();

    return (
        <header className="bg-blue-600 text-white p-4 flex justify-between items-center">
            <div>
                <h1 className="text-2xl font-bold">Chat Application</h1>
                {username && <p className="text-sm text-blue-100">Logged in as: {username}</p>}
            </div>
            {username && (
                <button
                    onClick={logout}
                    className="bg-blue-700 hover:bg-blue-800 px-3 py-1 rounded text-sm font-medium transition"
                >
                    Logout
                </button>
            )}
        </header>
    );  
}
export default Header;