interface InputFieldProps {
  placeholderText: string;
  userInput: string;
  setUserInput: React.Dispatch<React.SetStateAction<string>>;
  width: number;
  height: number;
}

function InputField({
  placeholderText,
  userInput,
  setUserInput,
  width,
  height,
}: InputFieldProps) {
  return (
    <input
      style={{ width: width, height: height }}
      className="bg-white text-3xl placeholder-gray-400 text-sky-950 p-5 rounded-3xl border-6 border-sky-950 text-center hover:cursor-pointer hover:border-sky-900"
      placeholder={placeholderText}
      value={userInput}
      onChange={(e) => setUserInput(e.target.value)}
    ></input>
  );
}

export default InputField;
