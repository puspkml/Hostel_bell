import { json } from "@sveltejs/kit";
import axios from "axios";

export async function GET() {
    return json({ message: "Manual control endpoint ready. Use POST for emergency bell." });
}

export async function POST() {
    try {
        // List of ESP IPs to trigger simultaneously
        const espIPs = [
            
            "10.110.231.128"
        ];

        console.log(`Triggering direct bell ring at ${espIPs.length} ESPs:`, espIPs);
        let successCount = 0;
        const errors = [];

        // Make parallel GET requests to all IPs for simultaneous triggering
        const promises = espIPs.map(async (ip) => {
            try {
                const response = await axios.get(`http://${ip}/`, { timeout: 5000 });
                if (response.status === 200) {
                    console.log(`Direct trigger successful for ${ip}:`, response.statusText);
                    return { ip, success: true };
                } else {
                    console.error(`Direct trigger failed for ${ip} with status:`, response.status);
                    return { ip, success: false, error: `Status ${response.status}` };
                }
            } catch (err) {
                const errorMsg = err.message || err.toString();
                console.error(`Direct trigger error for ${ip} (e.g., offline or unreachable):`, errorMsg);
                return { ip, success: false, error: errorMsg };
            }
        });

        // Wait for all requests to complete (parallel)
        const results = await Promise.all(promises);
        successCount = results.filter(r => r.success).length;

        // Collect errors for logging
        errors.push(...results.filter(r => !r.success).map(r => `${r.ip}: ${r.error}`));

        // Prepare response message
        const total = espIPs.length;
        let message;
        if (successCount === total) {
            message = `Direct bell trigger sent successfully to all ${total} bells!`;
        } else if (successCount > 0) {
            message = `Direct bell trigger sent to ${successCount}/${total} bells (some offline).`;
        } else {
            message = `Direct bell trigger attempted on ${total} bells, but all failed (check connectivity).`;
        }

        // Optional: Log errors summary
        if (errors.length > 0) {
            console.log("Errors summary:", errors.join('; '));
        }

        return json({
            success: successCount > 0,  // True if at least one succeeded
            message: message,
            details: {
                triggered: successCount,
                total: total,
                failed: errors.length > 0 ? errors : undefined
            }
        });

    } catch (error) {
        console.error('Unexpected error:', error);
        return json({ success: false, message: 'Unexpected error: ' + error }, { status: 500 });
    }
}
