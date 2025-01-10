/*
 * Copyright (c) 2013 John May <jwmay@users.sf.net>
 *
 * Contact: cdk-devel@lists.sourceforge.net
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public License
 * as published by the Free Software Foundation; either version 2.1
 * of the License, or (at your option) any later version.
 * All we ask is that proper credit is given for our work, which includes
 * - but is not limited to - adding the above copyright notice to the beginning
 * of your source code files, and to any copyright notice that you may distribute
 * with programs based on this work.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 U
 */

namespace NCDK.Hash.Stereo
{
    /// <summary>
    /// Calculate the permutation parity on a given array of current values.
    /// </summary>
    /// <seealso href="http://en.wikipedia.org/wiki/Parity_of_a_permutation">Parity of a Permutation, Wikipedia</seealso>
    // @author John May
    // @cdk.module hash
    internal abstract class PermutationParity
    {
        /// <summary>
        /// Identity parity which always returns 1 (even). This is useful for
        /// configurations which do not require ordering, such as, double bonds with
        /// implicit hydrogens.
        /// </summary>
        public static readonly PermutationParity Identity = new EevenPermutationParity();

        class EevenPermutationParity : PermutationParity
        {
            public override int Parity(long[] current)
            {
                return 1;
            }
        }

        /// <summary>
        /// Calculate the permutation parity of a permutation on the current values.
        /// The inversion parity counts whether we need to do an odd or even number
        /// of swaps to put the values in sorted order. If the values contain
        /// duplicates then the parity is returned as 0.
        /// </summary>
        /// <param name="current">current values of invariants</param>
        /// <returns>-1, odd number of swaps, +1, even number of swaps, 0, contains duplicates</returns>
        public abstract int Parity(long[] current);
    }
}
