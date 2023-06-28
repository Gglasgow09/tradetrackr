import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

function OverallPerformance() {
    const [trades, setTrades] = useState([]);
    const [portfolioValue, setPortfolioValue] = useState(0);
    const [pnl, setPnl] = useState(0);
    const [roi, setRoi] = useState(0);
    const [winRate, setWinRate] = useState(0);
    const [maxDrawdown, setMaxDrawdown] = useState(0);
    const { userId } = useParams();

    useEffect(() => {
        const fetchTrades = () => {
            fetch(`/trade/users/${userId}`)
                .then((response) => response.json())
                .then((data) => setTrades(data))
                .catch((error) => console.error("Error fetching trades:", error));
        };

        fetchTrades();
    }, [userId]);

    useEffect(() => {
        const calculatePerformanceMetrics = () => {
            // Calculate portfolio value
            const totalPnl = trades.reduce((total, trade) => total + parseFloat(trade.pnl), 0);
            const startingCapital = 100000; // Assuming a starting capital of $100,000
            const currentPortfolioValue = startingCapital + totalPnl;
            setPortfolioValue(currentPortfolioValue);

            // Calculate total P&L
            setPnl(totalPnl);

            // Calculate ROI (Return on Investment)
            const roiValue = (totalPnl / startingCapital) * 100;
            setRoi(roiValue);

            // Calculate win rate
            const winTrades = trades.filter((trade) => parseFloat(trade.pnl) > 0);
            const winRateValue = (winTrades.length / trades.length) * 100;
            setWinRate(winRateValue);

            // Calculate max drawdown
            let maxDrawdownValue = 0;
            let peakValue = 0;
            let drawdownValue = 0;

            for (let i = 0; i < trades.length; i++) {
                const trade = trades[i];
                const tradePnl = parseFloat(trade.pnl);

                if (i === 0) {
                    peakValue = tradePnl;
                    maxDrawdownValue = 0;
                } else {
                    if (tradePnl > peakValue) {
                        peakValue = tradePnl;
                        drawdownValue = 0;
                    } else {
                        drawdownValue = peakValue - tradePnl;
                    }

                    if (drawdownValue > maxDrawdownValue) {
                        maxDrawdownValue = drawdownValue;
                    }
                }
            }

            setMaxDrawdown(maxDrawdownValue);
        };

        calculatePerformanceMetrics();
    }, [trades]);

    return (
        <div>
            <h1>Overall Performance</h1>
            <p>Portfolio Value: ${portfolioValue.toFixed(2)}</p>
            <p>P&L: ${pnl.toFixed(2)}</p>
            <p>ROI: {roi.toFixed(2)}%</p>
            <p>Win Rate: {winRate.toFixed(2)}%</p>
            <p>Max Drawdown: ${maxDrawdown.toFixed(2)}</p>
        </div>
    );
}

export default OverallPerformance;
