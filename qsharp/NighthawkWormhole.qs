namespace Sovereign.QuantumCentric {
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Measurement;

    /// Simulates a wormhole (teleportation) transaction across
    /// modular Nighthawk QPUs by recursive state injection.
    operation NighthawkWormholeTransaction() : Unit {

        let evolutionaryEpochs = [
            "Hollerith/Tabulating/Punched Card",
            "C-T-R/IBM/Mainframe/System/360",
            "FORTRAN/COBOL/Database/Relational/SQL",
            "Virtualization/Linux/HPC/AI/GPU",
            "Qiskit/Error Correction/Logical Qubit",
            "Nighthawk/Starling/Blue Jay/2033"
        ];

        let epochs = Length(evolutionaryEpochs);

        use (payload, localNode, remoteNode) = (Qubit(), Qubit(), Qubit());

        for i in 0 .. epochs - 1 {
            let theta = (PI() * IntAsDouble(i + 1)) / IntAsDouble(epochs);
            Ry(theta, payload);

            H(localNode);
            CNOT(localNode, remoteNode);

            CNOT(payload, localNode);
            H(payload);

            let mPayload = MResetZ(payload);
            let mLocal = MResetZ(localNode);

            if mLocal == One { X(remoteNode); }
            if mPayload == One { Z(remoteNode); }

            Message($"[Wormhole Tx {i}] Collapsed & Reconstructed Epoch: {evolutionaryEpochs[i]}");

            Reset(remoteNode);
        }
    }
}
