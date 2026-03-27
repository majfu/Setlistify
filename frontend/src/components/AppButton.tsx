interface AppButtonProps {
  text: string;
  width: number;
  height: number;
}

function AppButton({ text, width, height }: AppButtonProps) {
  return (
    <button
      style={{ width: width, height: height }}
      className="bg-sky-950 text-white rounded-3xl text-2xl hover:bg-sky-900 hover:cursor-pointer m-10"
    >
      {text}
    </button>
  );
}

export default AppButton;
