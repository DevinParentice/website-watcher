import MainTable from "@/components/MainTable";
import Navbar from "@/components/Navbar";

export default async function Home() {
	const data = await getData();
	return (
		<main className="min-h-screen flex flex-col items-center w-full h-full">
			<Navbar />
			<MainTable data={data} />
		</main>
	);
}

async function getData() {
	const res = await fetch("http://127.0.0.1:5000/api/getMonitors");

	if (!res.ok) {
		throw new Error("Failed to fetch monitors");
	}
	return res.json();
}
