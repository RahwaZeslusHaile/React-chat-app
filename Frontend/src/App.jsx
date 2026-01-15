import ChatWindow from "./components/ChatWindow.jsx";
function App() {
  return (
    <div className="flex justify-center items-start min-h-screen bg-gray-100 p-6">
      <div className="w-full max-w-sm h-[700px] bg-white shadow-xl rounded-3xl flex flex-col overflow-hidden">
        <ChatWindow> 
          
        </ChatWindow>
      </div>
    </div>
  );
}

export default App;
