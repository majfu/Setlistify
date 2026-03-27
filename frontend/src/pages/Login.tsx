import AppButton from "../components/AppButton";

function Login() {
  return (
    <div className="flex flex-col items-center justify-around">
      <div className="text-5xl mb-50 bg-sky-100 rounded-3xl p-20">
        Welcome to SetListify!
      </div>
      <div className="mb-20">Log in to get started</div>
      <AppButton text="Log In" width={800} height={100} />
    </div>
  );
}
export default Login;
