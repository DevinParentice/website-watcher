"use client";

import Monitors from "@/components/Monitors";
import NewMonitorPopup from "@/components/NewMonitorPopup";

import { useState } from "react";

export default function MainTable({ data }) {
	const [modalIsOpen, setModalIsOpen] = useState(false);
	const [monitors, setMonitors] = useState(data);

	return (
		<>
			<div className="w-1/2 min-h-[24rem] bg-zinc-800 rounded-2xl">
				<div className="flex justify-between items-center m-4">
					<h2 className="text-xl">{"// Monitors"}</h2>
					<button
						className="bg-blue-500 py-1 px-4 rounded-md"
						onClick={() => setModalIsOpen((currentState) => !currentState)}
					>
						Add <span className="font-extrabold text-xl">+</span>
					</button>
				</div>
				<Monitors monitors={monitors} setMonitors={setMonitors} />
			</div>
			{modalIsOpen && (
				<NewMonitorPopup
					setModalIsOpen={setModalIsOpen}
					setMonitors={setMonitors}
				/>
			)}
		</>
	);
}
