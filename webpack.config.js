const { watch } = require("fs");
const path = require("path");
const TerserPlugin = require("terser-webpack-plugin");

module.exports = {
    watch: true,
    entry: {
        signup: "./frontend/ts/signup.ts",
        signin: "./frontend/ts/signin.ts",
    },
    output: {
        filename: "[name].min.js",
        path: path.resolve(__dirname, "frontend/static/js"),
    },
    resolve: {
        extensions: [".ts", ".js"],
    },
    module: {
        rules: [
            {
                test: /\.ts$/,
                use: "ts-loader",
                exclude: /node_modules/,
            },
        ],
    },
    optimization: {
        minimize: true,
        minimizer: [new TerserPlugin()],
    },
    mode: "production",
};
