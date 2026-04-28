window.PROJECTS_DATA = [
	{
		id: "cirstag",
		title: "CirSTAG",
		track: "Research",
		venue: "DAC 2025 | Best Paper Nominee",
		impact: "Best Paper Nominee with 20% stronger attack error and 50% lower defense error in GNN stability analysis.",
		summary:
			"A spectral and probabilistic framework for graph neural network stability analysis, extending from circuit design workflows to recommendation-style graph systems.",
		tags: ["GNN Stability", "Probabilistic Graphs", "EDA"],
		artLabel: "GNN / Stability",
		featured: true,
		links: []
	},
	{
		id: "ood-diffusion",
		title: "OOD Robustness with Diffusion Models",
		track: "Industrial AI",
		venue: "KLA Corporation | 2024-Present",
		impact: "40% in-distribution improvement and 25% OOD improvement for high-dimensional spectra prediction.",
		summary:
			"Built a conditional diffusion pipeline for generating extremely high-dimensional out-of-distribution spectra in an industrial multi-label regression setting.",
		tags: ["Diffusion", "OOD Robustness", "Industrial Metrology"],
		artLabel: "OOD / Diffusion",
		featured: true,
		links: []
	},
	{
		id: "talking-heads",
		title: "Real-Time Talking Heads from User-Uploaded Avatars",
		track: "Generative AI",
		venue: "CVPR 2024 Demo",
		impact: "Real-time talking avatars driven by arbitrary audio and extended with live LLM conversations.",
		summary:
			"Developed a system that generates synchronized talking heads from a single uploaded avatar image, enabling interactive avatar-based communication for media, education, and customer support.",
		tags: ["AIGC", "Talking Avatar", "Real-Time Inference"],
		artLabel: "Avatar / Live",
		featured: true,
		links: [
			{
				label: "Video",
				url: "https://drive.google.com/file/d/1HsqRwAYIS7WWpbNsqjjuBPfROzYh0opo/view?usp=sharing"
			}
		]
	},
	{
		id: "spade",
		title: "SPADE",
		track: "Research",
		venue: "ICML 2021",
		impact: "Up to 18% better accuracy than vanilla PGD training when used for adversarial robustness guidance.",
		summary:
			"A black-box adversarial robustness metric that studies graph-based input and output manifolds to reveal both model stability and sample-level robustness.",
		tags: ["Adversarial Robustness", "Graph Manifolds", "Black-Box Evaluation"],
		image: "images/SPADE.png?v=20260428e",
		featured: false,
		links: [
			{
				label: "Paper",
				url: "https://arxiv.org/abs/2102.03716"
			}
		]
	},
	{
		id: "sgm-pinn",
		title: "SGM-PINN",
		track: "Research",
		venue: "DAC 2024",
		impact: "Up to 50% faster convergence for PINN training on CFD workloads.",
		summary:
			"Used probabilistic graphical models to drive importance sampling for physics-informed neural network training, reducing the amount of redundant data processed in each epoch.",
		tags: ["PINN", "Sampling", "Training Efficiency"],
		image: "images/SGM-PINN.png?v=20260428e",
		featured: false,
		links: []
	},
	{
		id: "avatar-agent",
		title: "AI Agent for Education, Entertainment, and Company in VR",
		track: "Generative AI",
		venue: "Stealth Startup | 2023-2024",
		impact: "82% emotion recognition accuracy across 27 emotions, 4.4 MOS, and 0.014 real-time factor in speech generation.",
		summary:
			"Served as scientific advisor and AI lead for 3D avatar assistants combining NLP, emotion recognition, speech synthesis, facial reconstruction, LLM dialogue, and real-time lip sync.",
		tags: ["LLM", "Emotion Recognition", "3D Avatar"],
		artLabel: "VR / Agent",
		featured: false,
		links: []
	},
	{
		id: "sagram",
		title: "SAGRAM",
		track: "Research",
		venue: "Research Prototype",
		impact: "Efficient coreset selection that improves training speed without sacrificing model quality.",
		summary:
			"A black-box coreset selection algorithm based on Gaussian graphical models for accelerating training while preserving downstream model quality.",
		tags: ["Coreset Selection", "Gaussian Graphs", "Efficiency"],
		image: "images/SAGRAM.png?v=20260428e",
		featured: false,
		links: []
	},
	{
		id: "hair-detection",
		title: "Hair Detection Stability Improvement",
		track: "Industrial AI",
		venue: "LEMA (Beijing) Technology Co., Ltd.",
		impact: "99.97% accuracy on a 200-image dataset with stable performance under severity-5 corruption.",
		summary:
			"Applied robust training and augmentation to a tiny industrial dataset, producing a vision model that stayed reliable under realistic perturbations such as blur and lighting shifts.",
		tags: ["Robust Vision", "Small Data", "Industrial Deployment"],
		image: "images/hair.png?v=20260428e",
		featured: false,
		links: [
			{
				label: "Company",
				url: "http://www.lemabj.com/"
			}
		]
	},
	{
		id: "vial-classification",
		title: "Vial Classification Accuracy and Runtime Improvement",
		track: "Industrial AI",
		venue: "LEMA (Beijing) Technology Co., Ltd.",
		impact: "42% accuracy lift and 5.8x runtime speedup over the previous production model.",
		summary:
			"Combined data selection, neural network pruning, augmentation, and robust training to improve both quality and throughput in an industrial classification pipeline.",
		tags: ["Model Compression", "Data Selection", "Production Vision"],
		image: "images/lema.png?v=20260428e",
		featured: false,
		links: [
			{
				label: "Company",
				url: "http://www.lemabj.com/"
			}
		]
	}
];
