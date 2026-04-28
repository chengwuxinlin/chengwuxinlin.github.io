window.PROJECTS_DATA = [
	{
		id: "cirstag",
		title: "CirSTAG",
		track: "Research",
		venue: "Graph stability research",
		impact: "A graph neural network stability project for circuit-style graph systems.",
		summary:
			"A spectral and probabilistic framework for studying when graph models remain stable and when they fail.",
		tags: ["GNN Stability", "Probabilistic Graphs", "EDA"],
		artLabel: "GNN / Stability",
		featured: true,
		links: []
	},
	{
		id: "ood-diffusion",
		title: "OOD Robustness with Diffusion Models",
		track: "Industrial AI",
		venue: "Applied robustness project",
		impact: "A diffusion-style pipeline for improving robustness under distribution shift.",
		summary:
			"Built conditional generative modeling tools for high-dimensional prediction settings where held-out examples can differ from training data.",
		tags: ["Diffusion", "OOD Robustness", "Industrial Metrology"],
		artLabel: "OOD / Diffusion",
		featured: true,
		links: []
	},
	{
		id: "talking-heads",
		title: "Real-Time Talking Heads from User-Uploaded Avatars",
		track: "Generative AI",
		venue: "Interactive media demo",
		impact: "Real-time talking avatars driven by arbitrary audio and extended with live LLM conversations.",
		summary:
			"Developed a system that generates synchronized talking heads from a single uploaded avatar image, enabling interactive avatar-based communication for media, education, and customer support.",
		tags: ["AIGC", "Talking Avatar", "Real-Time Inference"],
		artLabel: "Avatar / Live",
		featured: true,
		links: []
	},
	{
		id: "spade",
		title: "SPADE",
		track: "Research",
		venue: "Adversarial robustness research",
		impact: "A black-box metric for studying model and sample-level robustness.",
		summary:
			"A black-box adversarial robustness metric that studies graph-based input and output manifolds to reveal both model stability and sample-level robustness.",
		tags: ["Adversarial Robustness", "Graph Manifolds", "Black-Box Evaluation"],
		image: "images/SPADE.png?v=20260428",
		featured: false,
		links: []
	},
	{
		id: "sgm-pinn",
		title: "SGM-PINN",
		track: "Research",
		venue: "Training-efficiency research",
		impact: "A sampling method for reducing redundant training work in physics-informed models.",
		summary:
			"Used probabilistic graphical models to drive importance sampling for physics-informed neural network training, reducing the amount of redundant data processed in each epoch.",
		tags: ["PINN", "Sampling", "Training Efficiency"],
		image: "images/SGM-PINN.png?v=20260428",
		featured: false,
		links: []
	},
	{
		id: "avatar-agent",
		title: "AI Agent for Education, Entertainment, and Company in VR",
		track: "Generative AI",
		venue: "Avatar-agent prototype",
		impact: "A multimodal avatar-assistant system combining dialogue, speech, emotion, and animation components.",
		summary:
			"Designed 3D avatar-assistant components combining NLP, emotion recognition, speech synthesis, facial reconstruction, LLM dialogue, and real-time lip sync.",
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
		image: "images/SAGRAM.png?v=20260428",
		featured: false,
		links: []
	},
	{
		id: "hair-detection",
		title: "Hair Detection Stability Improvement",
		track: "Industrial AI",
		venue: "Robust vision project",
		impact: "A small-data vision project focused on stable behavior under realistic image perturbations.",
		summary:
			"Applied robust training and augmentation to a small industrial-style dataset with perturbations such as blur and lighting shifts.",
		tags: ["Robust Vision", "Small Data", "Industrial Deployment"],
		image: "images/industrial-vision.png?v=20260428",
		featured: false,
		links: []
	},
	{
		id: "vial-classification",
		title: "Vial Classification Accuracy and Runtime Improvement",
		track: "Industrial AI",
		venue: "Production-vision project",
		impact: "A model-quality and runtime improvement project for industrial image classification.",
		summary:
			"Combined data selection, neural network pruning, augmentation, and robust training to improve both quality and throughput in an industrial classification pipeline.",
		tags: ["Model Compression", "Data Selection", "Production Vision"],
		image: "images/industrial-classification.png?v=20260428",
		featured: false,
		links: []
	}
];
